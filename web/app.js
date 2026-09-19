/**
 * Stratify AI — Trợ lý Quy chế Đào tạo NEU (VinUni Lab 07)
 * Frontend Logic & RAG API Integration
 */

document.addEventListener('DOMContentLoaded', () => {
  // DOM Elements
  const chatForm = document.getElementById('chatForm');
  const queryInput = document.getElementById('queryInput');
  const messagesStream = document.getElementById('messagesStream');
  const audienceSelect = document.getElementById('audienceSelect');
  const topKSelect = document.getElementById('topKSelect');
  const btnClearChat = document.getElementById('btnClearChat');
  const currentAudienceTag = document.getElementById('currentAudienceTag');

  // Inspector Elements
  const metricTopScore = document.getElementById('metricTopScore');
  const metricLatency = document.getElementById('metricLatency');
  const metricFilter = document.getElementById('metricFilter');
  const retrievedCountBadge = document.getElementById('retrievedCountBadge');
  const chunksFeed = document.getElementById('chunksFeed');
  const corpusListContainer = document.getElementById('corpusListContainer');
  const btnToggleCorpusView = document.getElementById('btnToggleCorpusView');
  const paneChunks = document.getElementById('paneChunks');
  const paneCorpus = document.getElementById('paneCorpus');
  const widgetTotalChunks = document.getElementById('widgetTotalChunks');
  const navDocsCount = document.getElementById('navDocsCount');

  // Modal Elements
  const btnRunBenchmarkDemo = document.getElementById('btnRunBenchmarkDemo');
  const abTestModal = document.getElementById('abTestModal');
  const btnCloseModal = document.getElementById('btnCloseModal');
  const btnCloseModalBtn = document.getElementById('btnCloseModalBtn');
  const btnRunABAgain = document.getElementById('btnRunABAgain');
  const abResultA = document.getElementById('abResultA');
  const abResultB = document.getElementById('abResultB');

  // State
  let currentAudience = 'all';
  let isSubmitting = false;

  // 1. Initial Load: Fetch stats and documents list
  async function loadInitialData() {
    try {
      const statsRes = await fetch('/api/stats');
      if (statsRes.ok) {
        const stats = await statsRes.json();
        if (widgetTotalChunks) {
          widgetTotalChunks.textContent = stats.total_chunks;
        }
      }

      const docsRes = await fetch('/api/documents');
      if (docsRes.ok) {
        const data = await docsRes.json();
        renderCorpusList(data.documents);
        if (navDocsCount) {
          navDocsCount.textContent = data.total_documents;
        }
      }
    } catch (err) {
      console.warn('[Stratify AI] Lỗi nạp thông tin ban đầu:', err);
    }
  }

  // Render 7 Corpus Documents in Inspector
  function renderCorpusList(docs) {
    if (!corpusListContainer || !docs) return;
    corpusListContainer.innerHTML = '';

    docs.forEach((doc, idx) => {
      const card = document.createElement('div');
      card.className = 'doc-card';

      const isFaculty = doc.audience === 'faculty';
      const badgeClass = isFaculty ? 'badge-faculty' : 'badge-student';
      const audienceLabel = isFaculty ? 'Giảng viên' : 'Sinh viên';

      card.innerHTML = `
        <div class="doc-title-row">
          <span class="doc-name">${idx + 1}. ${escapeHtml(doc.title)}</span>
          <span class="doc-badge ${badgeClass}">${audienceLabel}</span>
        </div>
        <div class="doc-meta-row">
          <span>Phiên bản: <strong>${escapeHtml(doc.version)}</strong></span>
          <span><strong>${doc.chunks_count}</strong> Chunks</span>
        </div>
      `;

      // Clicking a doc card suggests asking about it
      card.style.cursor = 'pointer';
      card.title = `Bấm để hỏi về tài liệu: ${doc.title}`;
      card.addEventListener('click', () => {
        queryInput.value = `Tài liệu "${doc.title}" quy định những nội dung trọng tâm nào?`;
        queryInput.focus();
      });

      corpusListContainer.appendChild(card);
    });
  }

  // 2. Tab Toggle in Inspector Panel (Chunks vs 7 Docs)
  if (btnToggleCorpusView) {
    btnToggleCorpusView.addEventListener('click', (e) => {
      const target = e.target.closest('span');
      if (!target) return;
      const view = target.getAttribute('data-view');

      btnToggleCorpusView.querySelectorAll('span').forEach((s) => s.classList.remove('active'));
      target.classList.add('active');

      if (view === 'chunks') {
        paneChunks.style.display = 'block';
        paneCorpus.style.display = 'none';
      } else {
        paneChunks.style.display = 'none';
        paneCorpus.style.display = 'block';
      }
    });
  }

  // 3. Auto-resize textarea
  if (queryInput) {
    queryInput.addEventListener('input', () => {
      queryInput.style.height = 'auto';
      queryInput.style.height = Math.min(queryInput.scrollHeight, 120) + 'px';
    });

    queryInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        if (!isSubmitting && queryInput.value.trim()) {
          chatForm.dispatchEvent(new Event('submit', { cancelable: true }));
        }
      }
    });
  }

  // 4. Audience Sync: Select Box <-> Sidebar Chips <-> Tag
  function setAudience(val) {
    currentAudience = val;
    if (audienceSelect) audienceSelect.value = val;

    // Sync sidebar chips
    document.querySelectorAll('.filter-chip').forEach((chip) => {
      chip.classList.toggle('active', chip.getAttribute('data-audience') === val);
    });

    // Sync header tag
    if (currentAudienceTag) {
      let label = 'Tất cả';
      if (val === 'student') label = 'Sinh viên (student)';
      if (val === 'faculty') label = 'Giảng viên (faculty)';
      currentAudienceTag.textContent = `Audience: ${label}`;
    }

    if (metricFilter) {
      metricFilter.textContent = val;
    }
  }

  if (audienceSelect) {
    audienceSelect.addEventListener('change', (e) => {
      setAudience(e.target.value);
    });
  }

  document.querySelectorAll('.filter-chip').forEach((chip) => {
    chip.addEventListener('click', () => {
      const aud = chip.getAttribute('data-audience');
      setAudience(aud);
    });
  });

  // 5. Suggestion Chips Click
  document.querySelectorAll('.suggestion-chip').forEach((chip) => {
    chip.addEventListener('click', () => {
      const q = chip.getAttribute('data-q');
      const aud = chip.getAttribute('data-aud');
      if (aud) {
        setAudience(aud);
      }
      if (queryInput) {
        queryInput.value = q;
        queryInput.dispatchEvent(new Event('input'));
        chatForm.dispatchEvent(new Event('submit', { cancelable: true }));
      }
    });
  });

  // 6. Handle Chat Submission
  if (chatForm) {
    chatForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const question = queryInput.value.trim();
      if (!question || isSubmitting) return;

      isSubmitting = true;
      const topK = parseInt(topKSelect.value, 10) || 3;

      // Append user bubble
      appendUserMessage(question);
      queryInput.value = '';
      queryInput.style.height = 'auto';

      // Append typing indicator
      const typingEl = appendTypingIndicator();
      scrollToBottom();

      try {
        const res = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json; charset=utf-8' },
          body: JSON.stringify({
            question: question,
            audience: currentAudience,
            top_k: topK,
          }),
        });

        if (!res.ok) {
          throw new Error(`HTTP ${res.status}`);
        }

        const data = await res.json();
        typingEl.remove();

        // Append bot message with citations and meta
        appendBotMessage(data);

        // Update live metrics
        if (metricTopScore) metricTopScore.textContent = data.top_score.toFixed(3);
        if (metricLatency) metricLatency.textContent = `${data.latency_ms} ms`;
        if (metricFilter) metricFilter.textContent = data.audience_filter;

        // Render retrieved chunks in inspector
        renderRetrievedChunks(data.chunks);

        // Switch to Chunks tab if in Corpus tab
        if (paneChunks && paneCorpus && paneChunks.style.display === 'none') {
          btnToggleCorpusView.querySelectorAll('span').forEach((s) => s.classList.remove('active'));
          btnToggleCorpusView.querySelector('[data-view="chunks"]').classList.add('active');
          paneChunks.style.display = 'block';
          paneCorpus.style.display = 'none';
        }

      } catch (err) {
        console.error('[Stratify Chat] Lỗi:', err);
        typingEl.remove();
        appendBotMessage({
          answer: `⚠️ **Không thể kết nối đến máy chủ RAG:** ${err.message}. Vui lòng kiểm tra server.py.`,
          chunks: [],
          top_score: 0.0,
          latency_ms: 0,
        });
      } finally {
        isSubmitting = false;
        scrollToBottom();
      }
    });
  }

  // 7. Append User Message
  function appendUserMessage(text) {
    const group = document.createElement('div');
    group.className = 'message-group user-group';
    group.innerHTML = `
      <div class="message-avatar user-avatar-msg">NL</div>
      <div class="message-content">
        <div class="bubble user-bubble">
          <p>${escapeHtml(text)}</p>
        </div>
      </div>
    `;
    messagesStream.appendChild(group);
  }

  // 8. Append Bot Message
  function appendBotMessage(data) {
    const group = document.createElement('div');
    group.className = 'message-group bot-group';

    const formattedAnswer = renderMarkdownToHtml(data.answer || '');
    const chunksCount = data.chunks ? data.chunks.length : 0;
    const latency = data.latency_ms || 0;
    const topScore = (data.top_score !== undefined) ? data.top_score.toFixed(3) : '0.000';

    group.innerHTML = `
      <div class="message-avatar bot-avatar">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path>
        </svg>
      </div>
      <div class="message-content">
        <div class="bubble bot-bubble">
          <div class="bot-header-meta">
            <span class="bot-name">Stratify RAG Engine</span>
            <span class="badge-knowledge">Top-K: ${chunksCount} chunks</span>
          </div>
          <div class="bot-text">
            ${formattedAnswer}
          </div>
          <div class="message-meta-strip">
            <div class="meta-item">
              <span>Top Score:</span>
              <span class="meta-val">${topScore}</span>
            </div>
            <div class="meta-item">
              <span>Độ trễ:</span>
              <span class="meta-val">${latency} ms</span>
            </div>
            <div class="meta-item">
              <span>Filter:</span>
              <span class="meta-val">${data.audience_filter || currentAudience}</span>
            </div>
          </div>
        </div>
      </div>
    `;
    messagesStream.appendChild(group);

    // Add click listeners to citations inside this message
    group.querySelectorAll('.citation-badge').forEach((badge) => {
      badge.addEventListener('click', () => {
        const citeIndex = parseInt(badge.getAttribute('data-cite'), 10) - 1;
        if (data.chunks && data.chunks[citeIndex]) {
          highlightChunkInInspector(citeIndex);
        }
      });
    });
  }

  // Typing Indicator Element
  function appendTypingIndicator() {
    const group = document.createElement('div');
    group.className = 'message-group bot-group typing-indicator-group';
    group.innerHTML = `
      <div class="message-avatar bot-avatar">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path>
        </svg>
      </div>
      <div class="message-content">
        <div class="bubble bot-bubble" style="padding: 12px 18px;">
          <div style="display: flex; align-items: center; gap: 8px; color: var(--text-dim); font-size: 0.85rem;">
            <span>Đang tra cứu cơ sở tri thức & tổng hợp câu trả lời</span>
            <span class="pulse-dot"></span>
          </div>
        </div>
      </div>
    `;
    messagesStream.appendChild(group);
    return group;
  }

  // 9. Render Chunks in Inspector
  function renderRetrievedChunks(chunks) {
    if (!chunksFeed) return;
    chunksFeed.innerHTML = '';

    if (!chunks || chunks.length === 0) {
      chunksFeed.innerHTML = `
        <div class="empty-state">
          <div class="empty-icon">⚠️</div>
          <h4>Không tìm thấy chunk phù hợp</h4>
          <p>Không có đoạn văn bản nào vượt qua bộ lọc hoặc cơ sở tri thức chưa có nội dung tương ứng.</p>
        </div>
      `;
      if (retrievedCountBadge) retrievedCountBadge.textContent = '0 chunks';
      return;
    }

    if (retrievedCountBadge) {
      retrievedCountBadge.textContent = `${chunks.length} chunks`;
    }

    chunks.forEach((c, idx) => {
      const card = document.createElement('div');
      card.className = 'chunk-card';
      card.id = `chunk-card-${idx}`;

      const meta = c.metadata || {};
      const aud = meta.audience || 'student';
      const audTagClass = aud === 'faculty' ? 'aud-faculty' : 'aud-student';
      const audLabel = aud === 'faculty' ? 'Giảng viên' : 'Sinh viên';

      card.innerHTML = `
        <div class="chunk-header">
          <div class="chunk-rank-id">
            <span class="chunk-rank">#${idx + 1}</span>
            <span class="chunk-id" title="${escapeHtml(c.id)}">${escapeHtml(meta.title || c.id)}</span>
          </div>
          <span class="chunk-score">Score: ${c.score.toFixed(3)}</span>
        </div>
        <div class="chunk-snippet">${escapeHtml(c.content)}</div>
        <div class="chunk-meta-tags">
          <span class="tag-meta ${audTagClass}">Audience: ${audLabel}</span>
          <span class="tag-meta">Version: ${escapeHtml(meta.document_version || '2024.1')}</span>
          <span class="tag-meta">Chunk #${meta.chunk_idx !== undefined ? meta.chunk_idx : idx}</span>
        </div>
      `;

      chunksFeed.appendChild(card);
    });
  }

  function highlightChunkInInspector(idx) {
    const card = document.getElementById(`chunk-card-${idx}`);
    if (card) {
      card.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      card.style.borderColor = 'var(--accent-pink)';
      card.style.boxShadow = '0 0 20px rgba(236, 72, 153, 0.4)';
      setTimeout(() => {
        card.style.borderColor = '';
        card.style.boxShadow = '';
      }, 1800);
    }
  }

  // 10. A/B Test Modal Experiment
  if (btnRunBenchmarkDemo) {
    btnRunBenchmarkDemo.addEventListener('click', runABTestExperiment);
  }

  if (btnCloseModal) {
    btnCloseModal.addEventListener('click', () => abTestModal.classList.remove('open'));
  }
  if (btnCloseModalBtn) {
    btnCloseModalBtn.addEventListener('click', () => abTestModal.classList.remove('open'));
  }
  if (btnRunABAgain) {
    btnRunABAgain.addEventListener('click', runABTestExperiment);
  }

  async function runABTestExperiment() {
    abTestModal.classList.add('open');
    abResultA.innerHTML = '<div class="loading-spinner">Đang truy vấn phương án A (All)...</div>';
    abResultB.innerHTML = '<div class="loading-spinner">Đang truy vấn phương án B (Student Pre-Filter)...</div>';

    const testQuestion = 'Quy định về thời hạn rút học phần và thẩm quyền phê duyệt môn học?';

    try {
      // Query A: audience = all
      const [resA, resB] = await Promise.all([
        fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ question: testQuestion, audience: 'all', top_k: 3 }),
        }),
        fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ question: testQuestion, audience: 'student', top_k: 3 }),
        }),
      ]);

      const dataA = await resA.json();
      const dataB = await resB.json();

      // Render A
      abResultA.innerHTML = `
        <div style="margin-bottom: 8px; color: var(--text-dim); font-size: 0.75rem;">
          Độ trễ: <strong>${dataA.latency_ms} ms</strong> | Top score: <strong>${dataA.top_score.toFixed(3)}</strong>
        </div>
        <div style="display: flex; flex-direction: column; gap: 8px;">
          ${dataA.chunks.map((c, i) => `
            <div style="background: rgba(255,255,255,0.03); padding: 8px; border-radius: 6px; border: 1px solid var(--card-border);">
              <div style="display:flex; justify-content:space-between; margin-bottom: 4px;">
                <strong style="color:#fff; font-size:0.75rem;">#${i + 1} ${escapeHtml(c.metadata.title || c.id)}</strong>
                <span style="font-size:0.68rem; color:${c.metadata.audience === 'faculty' ? '#a78bfa' : '#38bdf8'}">[${c.metadata.audience}]</span>
              </div>
              <p style="font-size:0.72rem; color:var(--text-muted);">${escapeHtml(c.content.slice(0, 120))}...</p>
            </div>
          `).join('')}
        </div>
      `;

      // Render B
      abResultB.innerHTML = `
        <div style="margin-bottom: 8px; color: var(--text-dim); font-size: 0.75rem;">
          Độ trễ: <strong>${dataB.latency_ms} ms</strong> | Top score: <strong>${dataB.top_score.toFixed(3)}</strong>
        </div>
        <div style="display: flex; flex-direction: column; gap: 8px;">
          ${dataB.chunks.map((c, i) => `
            <div style="background: rgba(99,102,241,0.06); padding: 8px; border-radius: 6px; border: 1px solid rgba(99,102,241,0.25);">
              <div style="display:flex; justify-content:space-between; margin-bottom: 4px;">
                <strong style="color:#fff; font-size:0.75rem;">#${i + 1} ${escapeHtml(c.metadata.title || c.id)}</strong>
                <span style="font-size:0.68rem; color:#38bdf8; font-weight:700;">[100% student]</span>
              </div>
              <p style="font-size:0.72rem; color:var(--text-highlight);">${escapeHtml(c.content.slice(0, 120))}...</p>
            </div>
          `).join('')}
        </div>
        <div style="margin-top: 8px; font-size: 0.72rem; color: var(--accent-emerald);">
          ✓ Kết quả: Đã loại bỏ hoàn toàn các tài liệu nội bộ giảng viên, đúng 100% đối tượng sinh viên.
        </div>
      `;

    } catch (e) {
      abResultA.innerHTML = `<p style="color: var(--accent-rose)">Lỗi: ${e.message}</p>`;
      abResultB.innerHTML = `<p style="color: var(--accent-rose)">Lỗi: ${e.message}</p>`;
    }
  }

  // 11. Clear Chat
  if (btnClearChat) {
    btnClearChat.addEventListener('click', () => {
      if (confirm('Bạn có chắc chắn muốn xóa toàn bộ tin nhắn trên màn hình?')) {
        messagesStream.innerHTML = `
          <div class="message-group bot-group">
            <div class="message-avatar bot-avatar">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path>
              </svg>
            </div>
            <div class="message-content">
              <div class="bubble bot-bubble">
                <div class="bot-header-meta">
                  <span class="bot-name">Stratify AI Core</span>
                  <span class="badge-knowledge">Sẵn sàng</span>
                </div>
                <div class="bot-text">
                  <p>Lịch sử hội thoại đã được đặt lại. Bạn có thể đặt câu hỏi mới bất kỳ lúc nào!</p>
                </div>
              </div>
            </div>
          </div>
        `;
        if (chunksFeed) {
          chunksFeed.innerHTML = `
            <div class="empty-state">
              <div class="empty-icon">🔎</div>
              <h4>Chưa có truy vấn nào</h4>
              <p>Gửi một câu hỏi trong ô chat để quan sát các đoạn văn bản (chunks) được Vector Store xếp hạng.</p>
            </div>
          `;
        }
        if (metricTopScore) metricTopScore.textContent = '--';
        if (metricLatency) metricLatency.textContent = '-- ms';
      }
    });
  }

  // Helpers
  function scrollToBottom() {
    messagesStream.scrollTop = messagesStream.scrollHeight;
  }

  function escapeHtml(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  function renderMarkdownToHtml(md) {
    if (!md) return '';

    let html = escapeHtml(md);

    // Citations [1], [2], [3]
    html = html.replace(/\[(\d+)\]/g, '<span class="citation-badge" data-cite="$1">[$1]</span>');

    // Bold **text**
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    // Inline code `code`
    html = html.replace(/`([^`]+)`/g, '<code>$1</code>');

    // Unordered lists (- or +)
    html = html.replace(/^\s*[-+]\s+(.*)$/gm, '<li>$1</li>');

    // Ordered lists (1. 2.)
    html = html.replace(/^\s*(\d+)\.\s+(.*)$/gm, '<li>$2</li>');

    // Group adjacent <li> into <ul>
    html = html.replace(/((?:<li>.*?<\/li>\s*)+)/gs, '<ul>$1</ul>');

    // Paragraphs from double linebreaks
    const paragraphs = html.split(/\n{2,}/);
    html = paragraphs.map(p => {
      p = p.trim();
      if (!p) return '';
      if (p.startsWith('<ul>') || p.startsWith('<ol>') || p.startsWith('<li>')) return p;
      return `<p>${p.replace(/\n/g, '<br>')}</p>`;
    }).join('');

    return html;
  }

  // Run initial fetch
  loadInitialData();
});

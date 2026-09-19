/**
 * shadcn-ui/chatbot-template Frontend Logic
 * NEU Academic Regulations Assistant (VinUni Lab 07)
 */

document.addEventListener('DOMContentLoaded', () => {
  // DOM Elements
  const htmlEl = document.documentElement;
  const btnThemeToggle = document.getElementById('btnThemeToggle');
  const themeIconSun = document.getElementById('themeIconSun');
  const themeIconMoon = document.getElementById('themeIconMoon');
  const btnNewChat = document.getElementById('btnNewChat');
  const audienceSelect = document.getElementById('audienceSelect');
  const statusFilterTag = document.getElementById('statusFilterTag');

  const emptyState = document.getElementById('emptyState');
  const messagesStream = document.getElementById('messagesStream');
  const chatForm = document.getElementById('chatForm');
  const queryInput = document.getElementById('queryInput');
  const btnSend = document.getElementById('btnSend');

  // State
  let isBusy = false;
  let currentAudience = audienceSelect ? audienceSelect.value : 'student';

  // 1. Theme Toggle (Light / Dark)
  const savedTheme = localStorage.getItem('neu_rag_theme') || 'dark';
  setTheme(savedTheme);

  if (btnThemeToggle) {
    btnThemeToggle.addEventListener('click', () => {
      const nextTheme = htmlEl.classList.contains('dark') ? 'light' : 'dark';
      setTheme(nextTheme);
    });
  }

  function setTheme(theme) {
    if (theme === 'dark') {
      htmlEl.classList.add('dark');
      themeIconSun.classList.remove('hidden');
      themeIconMoon.classList.add('hidden');
    } else {
      htmlEl.classList.remove('dark');
      themeIconSun.classList.add('hidden');
      themeIconMoon.classList.remove('hidden');
    }
    localStorage.setItem('neu_rag_theme', theme);
  }

  // 2. Audience Selector Change
  if (audienceSelect) {
    audienceSelect.addEventListener('change', (e) => {
      currentAudience = e.target.value;
      let label = 'Tất cả';
      if (currentAudience === 'student') label = 'Sinh viên';
      if (currentAudience === 'faculty') label = 'Giảng viên';
      if (statusFilterTag) statusFilterTag.textContent = `Audience: ${label}`;
    });
  }

  // 3. New Chat Button
  if (btnNewChat) {
    btnNewChat.addEventListener('click', () => {
      if (confirm('Bắt đầu phiên hỏi đáp mới?')) {
        messagesStream.innerHTML = '';
        messagesStream.classList.add('hidden');
        emptyState.classList.remove('hidden');
        queryInput.value = '';
        queryInput.style.height = 'auto';
        btnSend.disabled = true;
      }
    });
  }

  // 4. Auto-resize Textarea & Input state
  if (queryInput) {
    queryInput.addEventListener('input', () => {
      queryInput.style.height = 'auto';
      queryInput.style.height = Math.min(queryInput.scrollHeight, 120) + 'px';
      btnSend.disabled = !queryInput.value.trim();
    });

    queryInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        if (!isBusy && queryInput.value.trim()) {
          chatForm.dispatchEvent(new Event('submit', { cancelable: true }));
        }
      }
    });
  }

  // 5. Suggestions Card Click
  document.querySelectorAll('.suggestion-card').forEach((card) => {
    card.addEventListener('click', () => {
      const q = card.getAttribute('data-q');
      const aud = card.getAttribute('data-aud');
      if (aud && audienceSelect) {
        audienceSelect.value = aud;
        audienceSelect.dispatchEvent(new Event('change'));
      }
      if (queryInput) {
        queryInput.value = q;
        queryInput.dispatchEvent(new Event('input'));
        chatForm.dispatchEvent(new Event('submit', { cancelable: true }));
      }
    });
  });

  // 6. Handle Form Submit
  if (chatForm) {
    chatForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const question = queryInput.value.trim();
      if (!question || isBusy) return;

      isBusy = true;
      btnSend.disabled = true;

      // Hide empty state, show messages stream
      emptyState.classList.add('hidden');
      messagesStream.classList.remove('hidden');

      // Append user message
      appendUserMessage(question);
      queryInput.value = '';
      queryInput.style.height = 'auto';

      // Append thinking indicator
      const thinkingEl = appendThinkingIndicator();
      window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });

      try {
        const res = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json; charset=utf-8' },
          body: JSON.stringify({
            question: question,
            audience: currentAudience,
            top_k: 3,
          }),
        });

        if (!res.ok) throw new Error(`HTTP ${res.status}`);

        const data = await res.json();
        thinkingEl.remove();

        appendAssistantMessage(data);
      } catch (err) {
        thinkingEl.remove();
        appendAssistantMessage({
          answer: `⚠️ **Không thể kết nối đến máy chủ:** ${err.message}. Vui lòng kiểm tra lại server.py.`,
          chunks: [],
          top_score: 0.0,
          latency_ms: 0,
        });
      } finally {
        isBusy = false;
        btnSend.disabled = !queryInput.value.trim();
        window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
      }
    });
  }

  // Helper: Append User Message
  function appendUserMessage(text) {
    const item = document.createElement('div');
    item.className = 'message-item user-message';
    item.innerHTML = `
      <div class="user-bubble">${escapeHtml(text)}</div>
    `;
    messagesStream.appendChild(item);
  }

  // Helper: Append Assistant Message with Accordion
  function appendAssistantMessage(data) {
    const item = document.createElement('div');
    item.className = 'message-item';

    const formattedAnswer = renderMarkdownToHtml(data.answer || '');
    const chunks = data.chunks || [];
    const topScore = data.top_score !== undefined ? data.top_score.toFixed(3) : '0.000';
    const latency = data.latency_ms || 0;

    let chunksAccordionHtml = '';
    if (chunks.length > 0) {
      chunksAccordionHtml = `
        <div class="chunks-accordion">
          <details>
            <summary class="chunks-accordion-summary">
              <span>Trích xuất ngữ cảnh (${chunks.length} Chunks • Top Score: ${topScore} • ${latency} ms)</span>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="6 9 12 15 18 9"></polyline>
              </svg>
            </summary>
            <div class="chunks-accordion-content">
              ${chunks.map((c, i) => `
                <div class="chunk-mini-card">
                  <div class="chunk-mini-header">
                    <span>#${i + 1} ${escapeHtml(c.metadata.title || c.id)}</span>
                    <span class="chunk-mini-score">Score: ${c.score.toFixed(3)}</span>
                  </div>
                  <div class="chunk-mini-snippet">${escapeHtml(c.content.slice(0, 180))}...</div>
                </div>
              `).join('')}
            </div>
          </details>
        </div>
      `;
    }

    item.innerHTML = `
      <div class="assistant-avatar">AI</div>
      <div class="assistant-content-wrapper">
        <div class="assistant-bubble">
          ${formattedAnswer}
        </div>
        ${chunksAccordionHtml}
      </div>
    `;

    messagesStream.appendChild(item);
  }

  // Helper: Append Thinking Indicator
  function appendThinkingIndicator() {
    const item = document.createElement('div');
    item.className = 'message-item';
    item.innerHTML = `
      <div class="assistant-avatar">AI</div>
      <div class="thinking-indicator">
        <span>Đang tra cứu và tổng hợp</span>
        <span class="pulse-dot"></span>
      </div>
    `;
    messagesStream.appendChild(item);
    return item;
  }

  // Markdown Parser
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
    html = html.replace(/\[(\d+)\]/g, '<span class="citation-chip">[$1]</span>');

    // Bold **text**
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    // Code `code`
    html = html.replace(/`([^`]+)`/g, '<code>$1</code>');

    // List items
    html = html.replace(/^\s*[-+]\s+(.*)$/gm, '<li>$1</li>');
    html = html.replace(/^\s*(\d+)\.\s+(.*)$/gm, '<li>$2</li>');
    html = html.replace(/((?:<li>.*?<\/li>\s*)+)/gs, '<ul>$1</ul>');

    // Paragraphs
    const paragraphs = html.split(/\n{2,}/);
    html = paragraphs.map(p => {
      p = p.trim();
      if (!p) return '';
      if (p.startsWith('<ul>') || p.startsWith('<ol>') || p.startsWith('<li>')) return p;
      return `<p>${p.replace(/\n/g, '<br>')}</p>`;
    }).join('');

    return html;
  }
});

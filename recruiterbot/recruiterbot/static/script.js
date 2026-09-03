const transcript = document.getElementById('transcript');
const composer = document.getElementById('composer');
const input = document.getElementById('question-input');
const sendButton = document.getElementById('send-button');

input.addEventListener('input', () => {
  input.style.height = 'auto';
  input.style.height = input.scrollHeight + 'px';
  sendButton.disabled = input.value.trim().length === 0;
});

input.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    composer.requestSubmit();
  }
});

composer.addEventListener('submit', async (e) => {
  e.preventDefault();
  const question = input.value.trim();
  if (!question) return;

  addQuestion(question);
  input.value = '';
  input.style.height = 'auto';
  setBusy(true);

  const typingEl = addTypingIndicator();

  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question }),
    });

    const data = await res.json();
    typingEl.remove();

    if (!res.ok) {
      addAnswer(data.error || "Something went wrong on my end — try again in a moment.", true);
    } else {
      addAnswer(data.answer, false);
    }
  } catch (err) {
    typingEl.remove();
    addAnswer("Couldn't reach the server — check your connection and try again.", true);
  } finally {
    setBusy(false);
    input.focus();
  }
});

function setBusy(busy) {
  input.disabled = busy;
  sendButton.disabled = busy || input.value.trim().length === 0;
}

function addQuestion(text) {
  const turn = document.createElement('div');
  turn.className = 'turn';
  const q = document.createElement('div');
  q.className = 'question';
  q.textContent = text;
  turn.appendChild(q);
  transcript.appendChild(turn);
  scrollToBottom();
  return turn;
}

function addAnswer(text, isError) {
  const wrap = document.createElement('div');
  wrap.className = 'answer' + (isError ? ' error' : '');

  const label = document.createElement('p');
  label.className = 'answer-label';
  label.textContent = isError ? 'error' : 'moez';
  wrap.appendChild(label);

  const body = document.createElement('p');
  body.textContent = text;
  wrap.appendChild(body);

  transcript.appendChild(wrap);
  scrollToBottom();
}

function addTypingIndicator() {
  const wrap = document.createElement('div');
  wrap.className = 'typing';
  wrap.innerHTML = '<span></span><span></span><span></span>';
  transcript.appendChild(wrap);
  scrollToBottom();
  return wrap;
}

function scrollToBottom() {
  transcript.scrollTop = transcript.scrollHeight;
}

sendButton.disabled = true;
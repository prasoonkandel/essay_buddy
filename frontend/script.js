import "./cursor.js";

const form = document.querySelector("#essay-form");
const topicInput = document.querySelector("#topic");
const descriptionInput = document.querySelector("#description");
const skeleton = document.querySelector("#skeleton");
const essayOutput = document.querySelector("#essay");
const outputCard = document.querySelector(".output-card");
const notice = document.querySelector("#notice");
const noticeMessage = document.querySelector("#notice-message");
const noticeCloseButton = document.querySelector("#notice-close");
const retryButton = document.querySelector("#retry-btn");
const generateButton = document.querySelector("#generate-btn");
const generateAnotherButton = document.querySelector("#generate-another");
const API_BASE_URL = (
  import.meta.env.API_BASE_URL || "https://essay-buddy.onrender.com"
)
  .trim()
  .replace(/\/$/, "");
const API_URL = `${API_BASE_URL}/api/generate-essay`;
const wordCountValue = document.querySelector("#word-count-value");

let lastPayload = null;
let noticeTimeout = null;
let lastEssayHtml = "";
let isFormCollapsed = false;

function setEssayVisibility(isVisible) {
  if (!essayOutput) {
    return;
  }

  essayOutput.classList.toggle("is-hidden", !isVisible);
  essayOutput.classList.toggle("is-visible", isVisible);
}

function setGenerateAnotherVisible(isVisible) {
  if (!generateAnotherButton) {
    return;
  }

  generateAnotherButton.classList.toggle("is-hidden", !isVisible);
}

function animateOutputCardHeight() {
  if (!outputCard || outputCard.classList.contains("is-hidden")) {
    return;
  }

  const startHeight = outputCard.getBoundingClientRect().height;
  outputCard.style.height = `${startHeight}px`;
  outputCard.style.overflow = "hidden";

  requestAnimationFrame(() => {
    const endHeight = outputCard.scrollHeight;
    outputCard.style.height = `${endHeight}px`;
  });

  outputCard.addEventListener(
    "transitionend",
    (event) => {
      if (event.propertyName !== "height") {
        return;
      }
      outputCard.style.height = "";
      outputCard.style.overflow = "";
    },
    { once: true },
  );
}

function updateOutputCardVisibility() {
  if (!outputCard || !skeleton || !essayOutput) {
    return;
  }

  const shouldShow =
    !skeleton.classList.contains("is-hidden") ||
    !essayOutput.classList.contains("is-hidden");
  outputCard.classList.toggle("is-hidden", !shouldShow);
  if (shouldShow) {
    animateOutputCardHeight();
  }
}

function setLoading(isLoading) {
  if (!form) {
    return;
  }

  form.classList.toggle("is-loading", isLoading);
  skeleton.classList.toggle("is-hidden", !isLoading);
  if (isLoading) {
    setEssayVisibility(false);
    setGenerateAnotherVisible(false);
  }
  updateOutputCardVisibility();
  setButtonsDisabled(isLoading);
}

function setFormCollapsed(shouldCollapse) {
  if (!form) {
    return;
  }

  isFormCollapsed = shouldCollapse;
  form.classList.toggle("is-collapsed", shouldCollapse);
}

function setButtonsDisabled(isDisabled) {
  [generateButton, generateAnotherButton, retryButton].forEach((button) => {
    if (button) {
      button.disabled = isDisabled;
    }
  });
}

function updateWordCountSummary() {
  if (!wordCountValue) {
    return;
  }

  const selected = document.querySelector("input[name='word_count']:checked");
  if (!selected) {
    wordCountValue.textContent = "500 words";
    return;
  }

  const labelText = selected.nextElementSibling?.textContent;
  wordCountValue.textContent = labelText || `${selected.value} words`;
}

function showNotice(message, variant, showRetry = false) {
  if (!notice || !noticeMessage) {
    return;
  }

  noticeMessage.textContent = message;
  notice.classList.remove("is-hidden", "is-fading");
  notice.classList.add("is-visible");
  notice.classList.toggle("is-error", variant === "error");
  notice.classList.toggle("is-success", variant === "success");
  if (retryButton) {
    retryButton.classList.toggle("is-hidden", !showRetry);
  }

  if (noticeTimeout) {
    clearTimeout(noticeTimeout);
  }

  if (variant === "error") {
    noticeTimeout = setTimeout(hideNotice, 3000);
  }
}

function hideNotice() {
  if (!notice || !noticeMessage) {
    return;
  }

  notice.classList.remove("is-visible");
  notice.classList.add("is-fading");

  setTimeout(() => {
    noticeMessage.textContent = "";
    notice.classList.add("is-hidden");
    notice.classList.remove("is-error", "is-success", "is-fading");
    if (retryButton) {
      retryButton.classList.add("is-hidden");
    }
  }, 280);

  if (noticeTimeout) {
    clearTimeout(noticeTimeout);
    noticeTimeout = null;
  }
}

function escapeHtml(value) {
  return value
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function renderMarkdown(markdown) {
  if (!markdown) {
    return "";
  }

  let text = escapeHtml(markdown);
  const codeBlocks = [];

  text = text.replace(/```([\s\S]*?)```/g, (match, code) => {
    const index = codeBlocks.length;
    codeBlocks.push(code.trim());
    return `{{CODE_BLOCK_${index}}}`;
  });

  const lines = text.split("\n");
  const output = [];
  let buffer = [];
  let inList = null;
  let inBlockquote = false;

  function flushParagraph() {
    if (buffer.length) {
      const paragraph = buffer.join(" ").trim();
      if (paragraph) {
        output.push(`<p>${parseInline(paragraph)}</p>`);
      }
      buffer = [];
    }
  }

  function closeList() {
    if (inList) {
      output.push(`</${inList}>`);
      inList = null;
    }
  }

  function closeBlockquote() {
    if (inBlockquote) {
      output.push("</blockquote>");
      inBlockquote = false;
    }
  }

  function parseInline(value) {
    return value
      .replace(/`([^`]+)`/g, "<code>$1</code>")
      .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
      .replace(/\*([^*]+)\*/g, "<em>$1</em>")
      .replace(/\[([^\]]+)\]\(([^)]+)\)/g, (match, label, url) => {
        return `<a href=\"${url}\" target=\"_blank\" rel=\"noopener noreferrer\">${label}</a>`;
      });
  }

  function parseTable(startIndex) {
    const header = lines[startIndex];
    const separator = lines[startIndex + 1];
    const rowLines = [];

    if (
      !separator ||
      !/^\s*\|?\s*:?[-]+:?\s*(\|\s*:?[-]+:?\s*)+\|?\s*$/.test(separator)
    ) {
      return null;
    }

    let index = startIndex + 2;
    while (index < lines.length && /\|/.test(lines[index])) {
      rowLines.push(lines[index]);
      index += 1;
    }

    const parseRow = (row) =>
      row
        .trim()
        .replace(/^\|/, "")
        .replace(/\|$/, "")
        .split("|")
        .map((cell) => parseInline(cell.trim()));

    const headerCells = parseRow(header);
    const rows = rowLines.map(parseRow);

    let tableHtml = "<table><thead><tr>";
    headerCells.forEach((cell) => {
      tableHtml += `<th>${cell}</th>`;
    });
    tableHtml += "</tr></thead><tbody>";
    rows.forEach((row) => {
      tableHtml += "<tr>";
      row.forEach((cell) => {
        tableHtml += `<td>${cell}</td>`;
      });
      tableHtml += "</tr>";
    });
    tableHtml += "</tbody></table>";
    return { tableHtml, nextIndex: index - 1 };
  }

  for (let i = 0; i < lines.length; i += 1) {
    const line = lines[i];
    const trimmed = line.trim();

    if (!trimmed) {
      flushParagraph();
      closeList();
      closeBlockquote();
      continue;
    }

    if (trimmed.startsWith("{{CODE_BLOCK_")) {
      flushParagraph();
      closeList();
      closeBlockquote();
      const index = Number(trimmed.match(/\d+/)?.[0]);
      const code = codeBlocks[index] || "";
      output.push(`<pre><code>${code}</code></pre>`);
      continue;
    }

    const headingMatch = trimmed.match(/^(#{1,6})\s+(.+)$/);
    if (headingMatch) {
      flushParagraph();
      closeList();
      closeBlockquote();
      const level = headingMatch[1].length;
      output.push(`<h${level}>${parseInline(headingMatch[2])}</h${level}>`);
      continue;
    }

    if (/^(-{3,}|_{3,}|\*{3,})$/.test(trimmed)) {
      flushParagraph();
      closeList();
      closeBlockquote();
      output.push("<hr />");
      continue;
    }

    if (trimmed.startsWith(">")) {
      flushParagraph();
      closeList();
      if (!inBlockquote) {
        output.push("<blockquote>");
        inBlockquote = true;
      }
      output.push(`<p>${parseInline(trimmed.replace(/^>\s?/, ""))}</p>`);
      continue;
    }

    if (/\|/.test(trimmed) && i + 1 < lines.length) {
      const tableData = parseTable(i);
      if (tableData) {
        flushParagraph();
        closeList();
        closeBlockquote();
        output.push(tableData.tableHtml);
        i = tableData.nextIndex;
        continue;
      }
    }

    const unorderedMatch = trimmed.match(/^[-*+]\s+(.+)$/);
    if (unorderedMatch) {
      flushParagraph();
      closeBlockquote();
      if (inList !== "ul") {
        closeList();
        output.push("<ul>");
        inList = "ul";
      }
      output.push(`<li>${parseInline(unorderedMatch[1])}</li>`);
      continue;
    }

    const orderedMatch = trimmed.match(/^\d+\.\s+(.+)$/);
    if (orderedMatch) {
      flushParagraph();
      closeBlockquote();
      if (inList !== "ol") {
        closeList();
        output.push("<ol>");
        inList = "ol";
      }
      output.push(`<li>${parseInline(orderedMatch[1])}</li>`);
      continue;
    }

    buffer.push(trimmed);
  }

  flushParagraph();
  closeList();
  closeBlockquote();

  return output
    .join("\n")
    .replace(/\{\{CODE_BLOCK_(\d+)\}\}/g, (match, index) => {
      const code = codeBlocks[Number(index)] || "";
      return `<pre><code>${code}</code></pre>`;
    });
}

function buildPayload() {
  const topic = topicInput.value.trim();
  const wordCountInput = document.querySelector(
    "input[name='word_count']:checked",
  );
  const wordCount = wordCountInput ? wordCountInput.value : "500";
  const extraInstructions = descriptionInput.value.trim();

  return {
    topic,
    word_count: wordCount,
    extra_instructions: extraInstructions,
  };
}

async function generateEssay(payload) {
  if (!payload || !payload.topic) {
    showNotice(
      "Please complete all required fields before generating an essay.",
      "error",
      false,
    );
    return;
  }

  hideNotice();
  if (essayOutput && !essayOutput.classList.contains("is-hidden")) {
    lastEssayHtml = essayOutput.innerHTML;
  }
  if (isFormCollapsed) {
    setFormCollapsed(false);
  }
  setLoading(true);
  lastPayload = payload;

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 20000);

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
      signal: controller.signal,
    });

    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
      let message =
        "Something went wrong while generating your essay. Please try again.";
      if (response.status === 400) {
        message =
          data.error ||
          "Please complete all required fields before generating an essay.";
      } else if (response.status === 429) {
        message =
          "You've reached the current generation limit. Please wait a moment and try again.";
      } else if (response.status >= 500) {
        message =
          "Something went wrong while generating your essay. Please try again.";
      }
      throw new Error(message);
    }

    if (!data.essay) {
      throw new Error("The essay response was empty. Please try again.");
    }

    if (essayOutput) {
      essayOutput.innerHTML = renderMarkdown(data.essay.trim());
    }
    setEssayVisibility(true);
    setGenerateAnotherVisible(true);
    setFormCollapsed(true);
    updateOutputCardVisibility();
    hideNotice();
  } catch (error) {
    if (error.name === "AbortError") {
      showNotice(
        "Essay generation is taking longer than expected. Please try again in a moment.",
        "error",
        true,
      );
    } else if (error.name === "TypeError") {
      showNotice(
        "Unable to connect to the server. Please check your internet connection and try again.",
        "error",
        true,
      );
    } else if (error.message) {
      showNotice(error.message, "error", true);
    } else {
      showNotice(
        "Unable to connect to the server. Please check your internet connection and try again.",
        "error",
        true,
      );
    }
    if (lastEssayHtml && essayOutput) {
      essayOutput.innerHTML = lastEssayHtml;
      setEssayVisibility(true);
      setGenerateAnotherVisible(true);
      updateOutputCardVisibility();
    } else {
      setFormCollapsed(false);
    }
  } finally {
    clearTimeout(timeoutId);
    setLoading(false);
  }
}

async function handleSubmit(event) {
  event.preventDefault();
  const payload = buildPayload();
  await generateEssay(payload);
}

if (form) {
  form.addEventListener("submit", handleSubmit);
}

if (generateAnotherButton) {
  generateAnotherButton.addEventListener("click", async () => {
    setFormCollapsed(false);
    setEssayVisibility(false);
    setGenerateAnotherVisible(false);
    updateOutputCardVisibility();
  });
}

if (retryButton) {
  retryButton.addEventListener("click", async () => {
    setFormCollapsed(false);
    const payload = lastPayload || buildPayload();
    updateOutputCardVisibility();
    await generateEssay(payload);
  });
}

if (noticeCloseButton) {
  noticeCloseButton.addEventListener("click", () => {
    hideNotice();
  });
}

function handleWordCountChange(event) {
  const target = event.target;
  if (!target || !target.matches("input[name='word_count']")) {
    return;
  }

  updateWordCountSummary();
  const details = target.closest("details");
  if (details) {
    details.removeAttribute("open");
  }
}

document.addEventListener("change", handleWordCountChange);
document.addEventListener("input", handleWordCountChange);
updateWordCountSummary();
updateOutputCardVisibility();

/**
 * Copy to LLM functionality for Spacelift documentation.
 * Binds click handler to pre-rendered button in HTML.
 */

(function() {
  'use strict';

  function attachHandlers() {
    const button = document.querySelector('.copy-to-llm-button');
    if (!button) {
      return;
    }

    // Remove any existing handlers to avoid duplicates
    const newButton = button.cloneNode(true);
    button.parentNode.replaceChild(newButton, button);

    // Add click handler
    newButton.addEventListener('click', handleCopyClick);
  }

  /**
   * Handle button click - copy markdown to clipboard
   */
  async function handleCopyClick(event) {
    const button = event.currentTarget;

    // Get the embedded markdown content from the hidden div
    const contentDiv = document.getElementById('llm-markdown-content');
    if (!contentDiv) {
      showToast('Error: Markdown content not found', 'error');
      return;
    }

    // Get content from data attribute (it's HTML-escaped, browser unescapes automatically)
    const markdownContent = contentDiv.dataset.content;
    if (!markdownContent) {
      showToast('Error: No markdown content available', 'error');
      return;
    }

    // Copy to clipboard
    try {
      await copyToClipboard(markdownContent);

      // Show success feedback
      button.classList.add('copied');
      showToast('Copied to clipboard!', 'success');

      // Reset button state after 2 seconds
      setTimeout(() => {
        button.classList.remove('copied');
      }, 2000);
    } catch (err) {
      showToast('Failed to copy to clipboard', 'error');
      console.error('Copy failed:', err);
    }
  }

  /**
   * Copy text to clipboard using modern API with fallback
   */
  async function copyToClipboard(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(text);
    }
    return fallbackCopyToClipboard(text);
  }

  /**
   * Fallback clipboard copy for older browsers
   */
  function fallbackCopyToClipboard(text) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();

    return new Promise((resolve, reject) => {
      try {
        const successful = document.execCommand('copy');
        document.body.removeChild(textArea);
        if (successful) {
          resolve();
        } else {
          reject(new Error('execCommand failed'));
        }
      } catch (err) {
        document.body.removeChild(textArea);
        reject(err);
      }
    });
  }

  /**
   * Show toast notification
   */
  function showToast(message, type = 'info') {
    const existingToast = document.querySelector('.copy-to-llm-toast');
    if (existingToast) {
      existingToast.remove();
    }

    const toast = document.createElement('div');
    toast.className = `copy-to-llm-toast copy-to-llm-toast--${type}`;
    toast.textContent = message;

    document.body.appendChild(toast);

    setTimeout(() => {
      toast.classList.add('show');
    }, 10);

    setTimeout(() => {
      toast.classList.remove('show');
      setTimeout(() => {
        toast.remove();
      }, 300);
    }, 3000);
  }

  // Attach handlers on initial load and instant navigation
  if (typeof document$ !== 'undefined') {
    document$.subscribe(attachHandlers);
  } else {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', attachHandlers);
    } else {
      attachHandlers();
    }
  }
})();

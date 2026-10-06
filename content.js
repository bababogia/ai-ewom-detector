// Function to instantly inject a loading badge and trigger the scan
function injectAndScan() {
    const reviews = document.querySelectorAll('[data-hook="review-body"], .review-text-content, div[data-hook="review-collapsed"], [data-hook="reviewRichContentContainer"]');

    reviews.forEach(reviewElement => {
        // Only target reviews that haven't been tagged yet
        if (!reviewElement.querySelector('.ewom-badge-container')) {
            
            // 1. Create the UI container and temporary loading badge
            const container = document.createElement('div');
            container.className = "ewom-badge-container";
            container.style.cssText = "margin-top: 12px; display: flex; align-items: center; gap: 8px; font-family: Arial, sans-serif;";

            const badge = document.createElement('div');
            badge.className = "ewom-result-badge";
            badge.style.cssText = "display: flex; padding: 4px 10px; font-size: 12px; font-weight: bold; border-radius: 12px; align-items: center; gap: 6px; background: #f3f4f6; color: #4b5563;";
            badge.innerHTML = `⏳ Scanning text...`;

            container.appendChild(badge);
            reviewElement.appendChild(container);

            // 2. Automatically trigger the AI analysis in the background
            analyzeText(reviewElement.innerText, badge);
        }
    });
}

// Function to handle the API call and update the UI
async function analyzeText(text, badgeElement) {
    try {
        const response = await fetch('http://127.0.0.1:8000/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: text })
        });
        const data = await response.json();
        const score = data.score;

        // 3. Transform the badge based on the real model's score
        if (score > 70) {
            badgeElement.style.background = "#fee2e2";
            badgeElement.style.color = "#991b1b";
            badgeElement.innerHTML = `⚠️ High AI Risk (${score}%)`;
        } else if (score > 40) {
            badgeElement.style.background = "#fef3c7";
            badgeElement.style.color = "#92400e";
            badgeElement.innerHTML = `⚡ Moderate AI Risk (${score}%)`;
        } else {
            badgeElement.style.background = "#dcfce7";
            badgeElement.style.color = "#166534";
            badgeElement.innerHTML = `✅ Likely Human (${score}%)`;
        }
    } catch (error) {
        badgeElement.style.background = "#fee2e2";
        badgeElement.style.color = "#991b1b";
        badgeElement.innerHTML = `❌ Server Offline`;
    }
}

// Run immediately and continuously watch the DOM
injectAndScan();
const observer = new MutationObserver(injectAndScan);
observer.observe(document.body, { childList: true, subtree: true });
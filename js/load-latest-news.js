// Load Latest News section dynamically from articles.json
async function loadLatestNews() {
    try {
        const response = await fetch('articles.json');
        const data = await response.json();
        const articles = data.articles;

        // Get articles 14-17 for latest news section (0-indexed: 13-16)
        const latestArticles = articles.slice(13, 17);

        // Find the Latest News section - look for the row that follows the "Latest News" section title
        const sectionTitles = document.querySelectorAll('.section-title h4');
        let latestNewsContainer = null;

        for (let title of sectionTitles) {
            if (title.textContent.trim() === 'Latest News') {
                // The container is the next sibling's next sibling (the row after section-title)
                const sectionTitleDiv = title.closest('.section-title');
                if (sectionTitleDiv && sectionTitleDiv.nextElementSibling) {
                    latestNewsContainer = sectionTitleDiv.nextElementSibling;
                }
                break;
            }
        }

        if (!latestNewsContainer) {
            console.error('Latest news container not found');
            return;
        }

        // Clear existing hardcoded content
        latestNewsContainer.innerHTML = '';

        // Create the latest news items
        latestArticles.forEach((article, index) => {
            const colClass = index < 2 ? 'col-lg-6' : 'col-lg-6'; // All are col-lg-6
            const articleHtml = `
                <div class="${colClass}">
                    <div class="position-relative mb-3">
                        <a href="article/${article.filename}">
                            <img class="img-fluid w-100" src="${article.image || 'img/placeholder.jpg'}" style="object-fit: cover;" alt="${article.title}">
                        </a>
                        <div class="bg-white border border-top-0 p-4">
                            <div class="mb-2">
                                <a class="badge badge-primary news-badge mr-2" href="news.html?category=${encodeURIComponent(article.category || 'News')}">${article.category || 'News'}</a>
                                <a class="text-body" href=""><small>${new Date(article.date).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })}</small></a>
                            </div>
                            <a class="h4 d-block mb-3 text-secondary text-uppercase font-weight-bold" href="article/${article.filename}">${article.title}</a>
                            <p class="m-0">${article.excerpt || article.content.substring(0, 150) + '...'}</p>
                        </div>
                        <div class="d-flex justify-content-between bg-white border border-top-0 p-4">
                            <div class="d-flex align-items-center">
                                <img class="rounded-circle mr-2" src="${article.authorImage || 'img/alfin.jpg'}" width="25" height="25" alt="${article.author || 'Author'}">
                                <small>${article.author || 'Alfin Syawalan'}</small>
                            </div>
                            <div class="d-flex align-items-center">
                                <small class="ml-3"><i class="far fa-eye mr-1"></i>${article.views || '0'}</small>
                                <small class="ml-3"><i class="far fa-comment mr-1"></i>${article.comments || '0'}</small>
                            </div>
                        </div>
                    </div>
                </div>
            `;

            latestNewsContainer.insertAdjacentHTML('beforeend', articleHtml);
        });

        // Add advertisement after the first two articles
        if (latestArticles.length >= 2) {
            const adHtml = `
                <div class="col-lg-12 mb-3">
                    <a href="https://htmlcodex.com/downloading/?item=1541"><img class="img-fluid w-100" src="img/ads-728x90.png" alt=""></a>
                </div>
            `;
            // Insert ad after the second article (index 1)
            const secondArticle = latestNewsContainer.children[1];
            if (secondArticle) {
                secondArticle.insertAdjacentHTML('afterend', adHtml);
            }
        }

        console.log('Latest news loaded successfully');

    } catch (error) {
        console.error('Error loading latest news:', error);
        // Fallback: keep existing content or show error message
    }
}

// Load latest news when DOM is ready
document.addEventListener('DOMContentLoaded', loadLatestNews);
async function loadNews() {

    const container = document.getElementById("news-container");


    try {

        const response = await fetch("/api/news");


        if (!response.ok) {

            throw new Error("News API error");

        }


        const news = await response.json();



        let html = "";



        news.slice(0, 6).forEach(article => {



            html += `

            <div class="news-card">


                <h2>
                    ${article.title}
                </h2>



                <p>
                    ${article.content.substring(0, 250)}...
                </p>



                <a 
                href="${article.url}" 
                target="_blank">

                    Read more

                </a>


            </div>


            `;


        });



        container.innerHTML = html;



    } catch (error) {


        console.error(
            "News loading error:",
            error
        );


        container.innerHTML = `

            <div class="news-error">

                ❌ Failed loading news

            </div>

        `;


    }


}



document.addEventListener(
    "DOMContentLoaded",
    loadNews
);
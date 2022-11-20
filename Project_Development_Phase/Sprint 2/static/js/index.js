const options = {
	method: 'GET',
    // headers : {
    //     'X-RapidAPI-Key': 'abb6f33b19msha2262373effcfc9p1fc02djsnd897b30a1368',
    //     'X-RapidAPI-Host': 'newscatcher.p.rapidapi.com'
    // }
    // headers: {
	// 	'X-RapidAPI-Key': '128edc7995msh1bfaeab1727ac96p1bd93ejsnd7936cb441ee',
	// 	'X-RapidAPI-Host': 'newscatcher.p.rapidapi.com'
	// }
    headers: {
		'X-RapidAPI-Key': '1faf7042f7msh25dfe6cd0895e2cp1b0845jsn533ff3867f6f',
		'X-RapidAPI-Host': 'newscatcher.p.rapidapi.com'
	}
};

// variables
const generalBtn = document.getElementById("genral");
const businessBtn = document.getElementById("business");
const sportsBtn = document.getElementById("sport");
const entertainmentBtn = document.getElementById("entertainment");
const technologyBtn = document.getElementById("technology");
const searchBtn = document.getElementById("searchBtn");
const newsQuery = document.getElementById("newsQuery");
const newsType = document.getElementById("newsType");
const newsdetails = document.getElementById("newsdetails");

// Array
var newsDataArr = [];

// apis 
const HEADLINES_NEWS = "https://newscatcher.p.rapidapi.com/v1/latest_headlines?topic=world&lang=en&media=True";
const GENERAL_NEWS = "https://newscatcher.p.rapidapi.com/v1/latest_headlines?topic=news&lang=en&media=True";
const BUSINESS_NEWS = "https://newscatcher.p.rapidapi.com/v1/latest_headlines?topic=business&lang=en&media=True";
const SPORTS_NEWS = "https://newscatcher.p.rapidapi.com/v1/latest_headlines?topic=sport&lang=en&media=True";
const ENTERTAINMENT_NEWS = "https://newscatcher.p.rapidapi.com/v1/latest_headlines?topic=entertainment&lang=en&media=True";
const TECHNOLOGY_NEWS = "https://newscatcher.p.rapidapi.com/v1/latest_headlines?topic=tech&lang=en&media=True";
const SEARCH_NEWS = "https://newscatcher.p.rapidapi.com/v1/search?lang=en&media=True&sort_by=date&q=";

window.onload = function() {
    newsType.innerHTML="<h4>Headlines</h4>";
    fetchHeadlines();
};


generalBtn.addEventListener("click",function(){
    newsType.innerHTML="<h4>General news</h4>";
    fetchGeneralNews();
});

businessBtn.addEventListener("click",function(){
    newsType.innerHTML="<h4>Business</h4>";
    fetchBusinessNews();
});

sportsBtn.addEventListener("click",function(){
    newsType.innerHTML="<h4>Sports</h4>";
    fetchSportsNews();
});

entertainmentBtn.addEventListener("click",function(){
    newsType.innerHTML="<h4>Entertainment</h4>";
    fetchEntertainmentNews();
});

technologyBtn.addEventListener("click",function(){
    newsType.innerHTML="<h4>Technology</h4>";
    fetchTechnologyNews();
});

searchBtn.addEventListener("click",function(){
    newsType.innerHTML="<h4>Search : "+newsQuery.value+"</h4>";
    fetchQueryNews();
});

const fetchHeadlines = async () => {
    const response = await fetch(HEADLINES_NEWS,options);
    newsDataArr = [];
    if(response.status >=200 && response.status < 300) {
        console.log(response.status, response.statusText);
        const myJson = await response.json();
        newsDataArr = myJson.articles;
    } else {
        // handle errors
        console.log(response.status, response.statusText);
        newsdetails.innerHTML = "<h5>No data found.</h5>"
        return;
    }

    displayNews();
}


const fetchGeneralNews = async () => {
    const response = await fetch(GENERAL_NEWS, options);
    newsDataArr = [];
    if(response.status >=200 && response.status < 300) {
        const myJson = await response.json();
        newsDataArr = myJson.articles;
    } else {
        // handle errors
        console.log(response.status, response.statusText);
        newsdetails.innerHTML = "<h5>No data found.</h5>"
        return;
    }

    displayNews();
}

const fetchBusinessNews = async () => {
    const response = await fetch(BUSINESS_NEWS, options);
    newsDataArr = [];
    if(response.status >=200 && response.status < 300) {
        const myJson = await response.json();
        newsDataArr = myJson.articles;
    } else {
        // handle errors
        console.log(response.status, response.statusText);
        newsdetails.innerHTML = "<h5>No data found.</h5>"
        return;
    }

    displayNews();
}

const fetchEntertainmentNews = async () => {
    const response = await fetch(ENTERTAINMENT_NEWS ,options);
    newsDataArr = [];
    if(response.status >=200 && response.status < 300) {
        const myJson = await response.json();
        console.log(myJson);
        newsDataArr = myJson.articles;
    } else {
        // handle errors
        console.log(response.status, response.statusText);
        newsdetails.innerHTML = "<h5>No data found.</h5>"
        return;
    }

    displayNews();
}

const fetchSportsNews = async () => {
    
    const response = await fetch(SPORTS_NEWS, options);
    newsDataArr = [];
    if(response.status >=200 && response.status < 300) {
                const myJson = await response.json();
                console.log(myJson);
                newsDataArr = myJson.articles;
            } else {
                // handle errors
                console.log(response.status, response.statusText);
                newsdetails.innerHTML = "<h5>No data found.</h5>"
                return;
            } 

    displayNews();
}

const fetchTechnologyNews = async () => {
    const response = await fetch(TECHNOLOGY_NEWS ,options);
    newsDataArr = [];
    if(response.status >=200 && response.status < 300) {
        const myJson = await response.json();
        newsDataArr = myJson.articles;
    } else {
        // handle errors
        console.log(response.status, response.statusText);
        newsdetails.innerHTML = "<h5>No data found.</h5>"
        return;
    }

    displayNews();
}

const fetchQueryNews = async () => {

    if(newsQuery.value == null)
        return;
    
    value ='"'+newsQuery.value+'"'
    const response = await fetch(SEARCH_NEWS+value ,options);
    newsDataArr = [];
    if(response.status >= 200 && response.status < 300) {
        const myJson = await response.json();
        newsDataArr = myJson.articles;
    } else {
        //error handle
        console.log(response.status, response.statusText);
        newsdetails.innerHTML = "<h5>No data found.</h5>"
        return;
    }

    displayNews();
}

function displayNews() {

    newsdetails.innerHTML = "";

    // if(newsDataArr.length == 0) {
    //     newsdetails.innerHTML = "<h5>No data found.</h5>"
    //     return;
    // }

    newsDataArr.forEach(news => {

        var col = document.createElement('div');
        col.className="col-sm-12 col-md-4 col-lg-3 p-2 card";

        var card = document.createElement('div');
        card.className = "p-2";

        var image = document.createElement('img');
        image.setAttribute("height","matchparent");
        image.setAttribute("width","100%");
        image.src=news.media;

        var cardBody = document.createElement('div');
        
        var newsHeading = document.createElement('h5');
        newsHeading.className = "card-title";
        newsHeading.innerHTML = news.title;

        var dateHeading = document.createElement('h6');
        dateHeading.className = "text-primary";
        dateHeading.innerHTML = news.published_date;

        var discription = document.createElement('p');
        discription.className="text-muted";
        discription.innerHTML = news.summary;

        var link = document.createElement('a');
        link.className="btn btn-dark";
        link.setAttribute("target", "_blank");
        link.href = news.link;
        link.innerHTML="Read more";

        cardBody.appendChild(newsHeading);
        cardBody.appendChild(dateHeading);
        cardBody.appendChild(discription);
        cardBody.appendChild(link);

        card.appendChild(image);
        card.appendChild(cardBody);

        col.appendChild(card);

        newsdetails.appendChild(col);
    });

}
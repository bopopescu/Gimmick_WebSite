flag = false;


function addToFavourites(e, news_id) {
    if (window.flag) {
        return;
    }
    window.flag = true;
    // news_id = window.location.href.split('news_id=')[1][0];

    favourites_element = document.getElementById("favourites");
    favourites_img_element = document.getElementById("favourites_img");
    favourites = parseInt(favourites_element.innerHTML);
    document.getElementsByTagName("body")[0].style.cursor = "progress";
    $.post(
        "../../../news/",
        {
            'command': "change-favourites",
            'news_id': news_id
        },
        function (text) {
            console.log(text);
            if (text[0] === '+') {
                favourites_element.innerHTML = text.substring(1);
                favourites_img_element.style.visibility = "visible"
            } else if (text[0] === '-') {
                favourites_element.innerHTML = text.substring(1);
                favourites_img_element.style.visibility = "hidden"
            }
            document.getElementsByTagName("body")[0].style.cursor = "default";
            window.flag = false;
        }
    );
}
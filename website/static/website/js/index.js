flag = false;

function addToFavourites(e, news_id) {
    if (window.flag) {
        return;
    }
    window.flag = true;
    // news_id = window.location.href.split('news_id=')[1][0];

    favourites_element = document.getElementById(news_id);
    favourites_img_element = document.getElementById("bookmark_" + news_id);
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
                favourites_img_element.classList.replace("fa-bookmark", "fa-check-circle");
            } else if (text[0] === '-') {
                favourites_element.innerHTML = text.substring(1);
                favourites_img_element.classList.replace("fa-check-circle", "fa-bookmark");
            }else {
                window.flag = false;
                document.getElementsByTagName("body")[0].style.cursor = "default";
                location.href = '../../news/';
            }
            window.flag = false;
            document.getElementsByTagName("body")[0].style.cursor = "default";
        }
    );
}

function send_support_message(e) {
    var name_field = document.getElementById('name');
    var email_field = document.getElementById('email');
    var subject_field = document.getElementById('subject');
    var message_field = document.getElementById('message');
    document.getElementsByTagName("body")[0].style.cursor = "progress";
    $.post(
        "../../../",
        {
            'command': "send-support-message",
            'name': name_field.value,
            'email':email_field.value,
            'subject':subject_field.value,
            'message':message_field.value
        },
        function (text) {
            if (text === 'done') {
                console.log('Sent');
                alert('Message has been sent');
                document.getElementsByTagName("body")[0].style.cursor = "default";
            }
        }
    );
}
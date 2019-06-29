var username_field = document.getElementById('username-field');
var password_field = document.getElementById('password-field');
var username_div = document.getElementById('username-div');
var password_div = document.getElementById('password-div');
var body = document.getElementById('body');

function button_click() {
    let username = username_field.value.trim();
    let password = password_field.value;

    if (username === '') {
        setUsernameAlertValidate("Username is required");
        return;
    }
    if (password === '') {
        setPasswordAlertValidate("Password is required");
        return;
    }

    console.log("Button click");
    body.classList.add("loading");
    $.post(
        "",
        {
            'command': "is_user_exists",
            'username': username
        },
        function (text) {
            if (text === 'False') {
                body.classList.remove("loading");
                setUsernameAlertValidate("This user doesn't exist");
            } else if (text === 'True') {
                let encrypted_password = Crypto.MD5(password);
                $.post(
                    "",
                    {
                        'command': "login",
                        'username': username,
                        'password': encrypted_password
                    },
                    function (text) {
                        if (text === 'False') {
                            body.classList.remove("loading");
                            setPasswordAlertValidate("Wrong password");
                        } else if (text === 'True') {
                            document.location.href = "../../"
                        }
                    }
                );
            }
        }
    );

}

function removeUsernameAlertValidate() {
    username_div.classList.remove("alert-validate");
}

function removePasswordAlertValidate() {
    password_div.classList.remove("alert-validate");
}

function setUsernameAlertValidate(text) {
    username_div.setAttribute('data-validate', text);
    username_div.classList.add("alert-validate");
}

function setPasswordAlertValidate(text) {
    password_div.setAttribute('data-validate', text);
    password_div.classList.add("alert-validate");
}


function onEnterClicked(e) {
    if (e.keyCode === 13) {
        button_click();
    }
}

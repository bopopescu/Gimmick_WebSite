var username_field = document.getElementById('username-field');
var password_field = document.getElementById('password-field');
var repeat_password_field = document.getElementById('repeat-password-field');
var username_div = document.getElementById('username-div');
var password_div = document.getElementById('password-div');
var repeat_password_div = document.getElementById('repeat-password-div');
var body = document.getElementById('body');

function button_click() {
    removeUsernameAlertValidate();
    removePasswordAlertValidate();
    removeRepeatPasswordAlertValidate();
    username = username_field.value.trim();
    password = password_field.value;
    repeat_password = repeat_password_field.value;


    if (username === '') {
        setUsernameAlertValidate("Username is required");
        return;
    }else if(username.length < 8){
        setUsernameAlertValidate("Username is too short");
        return;
    }else if (password === '') {
        setPasswordAlertValidate("Password is required");
        return;
    } else if (password.length < 8) {
        setPasswordAlertValidate("Your password is too short");
        return;
    } else if(password.toLowerCase().includes(username.toLowerCase())){
        setPasswordAlertValidate("Your password shouldn't contain your username");
        return;
    }else if (!password.match("^.{8,}(?<=\\d.*)(?<=[^a-zA-Z0-9].*)$"))
    {
        setPasswordAlertValidate("Your password is too easy" +
            "\nIt should have:" +
            "\n1. At least 8 symbols; " +
            "\n2. At least one digit; " +
            "\n3. At least one non-letter-digit-symbol;");
        return;
    }else if (!(password === repeat_password)) {
        setRepeatPasswordAlertValidate("You entered two different passwords.");
        return;
    }

    body.classList.add("loading");
    $.post(
        "../../../auth/signup/",
        {
            'command': "is_user_exists",
            'username': username
        },
        function (text) {
            if (text === 'True') {
                body.classList.remove("loading");
                setUsernameAlertValidate("This user is already exist");
            } else if (text === 'False') {
                let encrypted_password = Crypto.MD5(password);
                $.post(
                    "../../../auth/signup/",
                    {
                        'command': "signup",
                        'username': username,
                        'password': encrypted_password
                    },
                    function (text) {
                        if (text === 'False') {
                            body.classList.remove("loading");
                            setUsernameAlertValidate("Some error occurred, try another username");
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

function removeRepeatPasswordAlertValidate() {
    repeat_password_div.classList.remove("alert-validate");
}

function setUsernameAlertValidate(text) {
    username_div.setAttribute('data-validate', text);
    username_div.classList.add("alert-validate");
}

function setPasswordAlertValidate(text) {
    password_div.setAttribute('data-validate', text);
    password_div.classList.add("alert-validate");
}

function setRepeatPasswordAlertValidate(text) {
    repeat_password_div.setAttribute('data-validate', text);
    repeat_password_div.classList.add("alert-validate");
}

function onEnterClicked(e) {
    if (e.keyCode === 13) {
        button_click();
    }
}

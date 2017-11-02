
       $(function () {
        $("#dialog").dialog({
            modal: true,
            autoOpen: false,
            title: "Add Author Window",
            width: 700,
            height: 500

        });
        $("#add_author").click(function () {
            $('#dialog').dialog('open');
        });
    });

  $(function () {
        $("#book_dialog").dialog({
            modal: true,
            autoOpen: false,
            title: "Add Book Window",
            width: 500,
            height: 700

        });
        $("#add_book").click(function () {
            $('#book_dialog').dialog('open');
        });
    });
  
 $(function () {
        $("#signup_dialog").dialog({
            modal: true,
            autoOpen: false,
            title: "Create an Account",
            width: 450,
            height: 550

        });
        $("#add_account").click(function () {
            $('#signup_dialog').dialog('open');
        });
    });



    $(function () {
        $("#login_dialog").dialog({
            modal: true,
            autoOpen: false,
            title: "Login",
            width: 500,
            height: 400
        });
        $("#btnShow2").click(function () {
            $('#login_dialog').dialog('open');
        });
    });

$("#logout").click(function(){
   location.assign("{% url 'logoutwindow' %}"); 
});
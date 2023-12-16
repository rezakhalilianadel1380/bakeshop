function showAndDismissAlert(type, message) {
    var htmlAlert = '<div class="alert alert-' + type + '"  style="height:70px">'+
        "<i class='bi bi-lightbulb-fill' style='color:yellow'></i> "
         + '<span> ' +message +' </span>'+ 
         
         '</div>';

    // Prepend so that alert is on top, could also append if we want new alerts to show below instead of on top.
    $(".alert-messages").prepend(htmlAlert);

    // Since we are prepending, take the first alert and tell it to fade in and then fade out.
    // Note: if we were appending, then should use last() instead of first()
    $(".alert-messages .alert").first().hide().fadeIn(200).delay(2000).fadeOut(1000, function () { $(this).remove(); });
}

function heart_icon_func(el,bread_id){
    var heart_icon=el.firstElementChild;
    if (heart_icon.classList.contains('bi-heart')) {
        heart_icon.classList.remove('bi-heart');
        heart_icon.classList.remove('text-white');
        heart_icon.classList.add('bi-heart-fill');
        heart_icon.classList.add('text-danger');
        $.ajax({
            url:'/add-to-favorite',
            headers: {'X-CSRFToken': csrftoken},
            type:'POST',
            data:{
                "bread_id":bread_id,
            },
            success:function(rsp){
                 showAndDismissAlert('green','با موفقیت به علاقه مندی ها اضافه شد ! ');
            },
        });
    } 
    else {
        heart_icon.classList.remove('bi-heart-fill');
        heart_icon.classList.add('bi-heart');
        heart_icon.classList.remove('text-danger');
        heart_icon.classList.add('text-dark');
        $.ajax({
            url:'/Delete-from-favorite',
            headers: {'X-CSRFToken': csrftoken},
            type:'POST',
            data:{
                "bread_id":bread_id,
            },
            success:function(rsp){
                showAndDismissAlert('red','از علاقه مندی ها حذف شد !  ');
            },
        });
       
    }
}

function getCookie(name) {
let cookieValue = null;
if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
        }
    }
}
    return cookieValue;
    }
const csrftoken = getCookie('csrftoken');

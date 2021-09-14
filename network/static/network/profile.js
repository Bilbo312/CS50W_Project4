document.addEventListener('DOMContentLoaded', function() {
    follow_username = document.getElementById('username').value;
    following_id = document.getElementById('fol_id').value;
    document.querySelector('#follow_btn').addEventListener('click', () => follow(follow_username,following_id));
  });

  function follow(username, following_id) {
    var btn_text = "";
    var action = "";
    const follow_text= document.querySelector('#follow_btn').innerHTML;
    if (follow_text=="Follow") {
        btn_text = "Unfollow",
        action = "Follow";
    }
    else {
        btn_text = "Follow",
        action = "Unfollow";
    }
    fetch(`/follow/${username}/${action}`,{
        method:'POST'
    })
    .then(response=> {response.json(),
        console.log(btn_text, following_id, status)}
        )
    .then(document.querySelector('#follow_btn').innerHTML = btn_text)
};
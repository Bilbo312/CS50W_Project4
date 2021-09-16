document.addEventListener('DOMContentLoaded', function() {
    // document.getElementById('btn').onclick = function() {
    //     document.getElementById('example').innerHTML = 'Help'
    // };
    document.querySelectorAll('.like_btn').forEach(link => {
        link.onclick = () => {
            const post_id = link.dataset.id;
            // document.getElementById('example').innerHTML = link.innerHTML;
            if(link.innerHTML === "Like")
            {
                document.querySelector(`#likes_${post_id}`).innerHTML++;
                link.innerHTML = "Unlike";
                const like = "like"
                like_status(post_id,like);
            }
            else
            {
                document.querySelector(`#likes_${post_id}`).innerHTML--;
                link.innerHTML = "Like";
                const unlike = "unlike"
                like_status(post_id,unlike);
            }
        }
    });
})

function like_status(post_id, status)
    {
        fetch(`/like/${post_id}/${status}`, {
            method: "POST"
        })
        .then(response => response.json())
        .then(data => console.log(data));
    }
document.addEventListener('DOMContentLoaded', function() {
    // document.getElementById('btn').onclick = function() {
    //     document.getElementById('example').innerHTML = 'Help'
    // };
    document.querySelectorAll('.edit_btn').forEach(link => {
        link.onclick = () => { 
            post_id = link.dataset.id;
            let a = link.parentElement.parentElement.parentElement.childNodes[1].childNodes[1];
            const original_text = a.innerHTML;

            // document.getElementById('example').innerHTML = link.innerHTML + " yeehaw " + post_id + original_text;
            if (link.innerHTML === 'Edit') {
                link.innerHTML = "Save Changes";
                let text_area = document.createElement('textarea');
                text_area.innerHTML = original_text
                text_area.id = 'content-edit';
                a.parentNode.replaceChild(text_area,a);
            }
            else { 
                //link.innerHTML = document.getElementById('content-edit').value + post_id;
                fetch( "/edit", {
                    method: "PUT",
                    body: JSON.stringify({
                        postid:`${post_id}`,
                        content: document.getElementById('content-edit').value,
                     })
                })
            }
        };
    })
})
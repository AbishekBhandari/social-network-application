function getCookie(name){
  const value = `;${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if(parts.length == 2) return parts.pop().split(';').shift();
}

function submitHandler(id) {
console.log(id);
const textareaValue = document.getElementById(`textarea_${id}`).value;
const content = document.getElementById(`content_${id}`);
const modal = document.getElementById(`modal_edit_post_${id}`);

fetch(`/edit/${id}`, {
    method: "POST",
    headers: {
        "Content-type": "application/json",
        "X-CSRFToken": getCookie("csrftoken")
    },
    body: JSON.stringify({
        content: textareaValue
    })
})
.then(response => response.json())
.then(result => {
    content.innerHTML = result.data;
    
    $(`#modal_edit_post_${id}`).modal('hide');

    setTimeout(() => {
        document.body.classList.remove('modal-open');
        document.querySelectorAll('.modal-backdrop').forEach(el => el.remove());
    }, 400);
})
.catch(error => console.error("Error:", error));
}

    
function toggleLike(id) {
  let likeButton = document.getElementById(id);
  let isLiked = likeButton.classList.contains("fa-thumbs-down");
  console.log(isLiked)
  
  let url = isLiked ? `/removelike/${id}` : `/addlike/${id}`;  // Define the appropriate URL

  fetch(url, {
      headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken") // Ensure CSRF token is included
      },
  })
  .then(response => response.json())
  .then(data => {
    
          let likeCountElement = document.getElementById(`likecount_${id}`);
          likeCountElement.innerText = data.like_count + " like"; // Update like count
          // Toggle button appearance
          if (data.isliked) {
              likeButton.classList.remove("fa-thumbs-up");
              likeButton.classList.add("fa-thumbs-down");
          } else {
              likeButton.classList.remove("fa-thumbs-down");
              likeButton.classList.add("fa-thumbs-up");
          }
  })
  .catch(error => console.error("Error:", error));
}
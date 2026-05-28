// StudySphere Interactive Asynchronous (AJAX) System
document.addEventListener("DOMContentLoaded", () => {
    // Helper to get CSRF token from cookies
    const getCookie = (name) => {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    };
    const csrftoken = getCookie('csrftoken');

    // 1. Like / Unlike Post AJAX
    document.body.addEventListener("click", async (e) => {
        const likeBtn = e.target.closest(".like-btn");
        if (!likeBtn) return;
        
        e.preventDefault();
        const postId = likeBtn.dataset.postId;
        const url = `/posts/${postId}/like/`;
        
        try {
            const response = await fetch(url, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrftoken,
                    "Content-Type": "application/json"
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                
                // Update active state
                if (data.liked) {
                    likeBtn.classList.add("liked");
                    likeBtn.querySelector("i").className = "fa-solid fa-heart";
                } else {
                    likeBtn.classList.remove("liked");
                    likeBtn.querySelector("i").className = "fa-regular fa-heart";
                }
                
                // Update live count text
                const countSpan = likeBtn.querySelector(".likes-count");
                if (countSpan) {
                    countSpan.textContent = `${data.likes_count} Like${data.likes_count !== 1 ? 's' : ''}`;
                }
            }
        } catch (error) {
            console.error("Error liking post:", error);
        }
    });

    // 2. Submit Comment AJAX
    document.body.addEventListener("submit", async (e) => {
        const commentForm = e.target.closest(".comment-input-form");
        if (!commentForm) return;
        
        e.preventDefault();
        const postId = commentForm.dataset.postId;
        const inputField = commentForm.querySelector(".comment-input-box");
        const commentText = inputField.value.trim();
        
        if (!commentText) return;
        
        const url = `/posts/${postId}/comment/`;
        
        try {
            const response = await fetch(url, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrftoken,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ text: commentText })
            });
            
            if (response.ok) {
                const data = await response.json();
                
                // Construct the comment card HTML
                const commentList = document.querySelector(`#comment-list-${postId}`);
                if (commentList) {
                    const commentItem = document.createElement("div");
                    commentItem.className = "comment-item";
                    commentItem.id = `comment-${data.id}`;
                    commentItem.style.opacity = "0";
                    commentItem.style.transform = "translateY(10px)";
                    commentItem.style.transition = "all 0.3s ease";
                    
                    commentItem.innerHTML = `
                        <img src="${data.profile_image}" alt="${data.username}" class="comment-avatar">
                        <div class="comment-details">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <span class="comment-user">${data.username}</span>
                                <button class="delete-comment-btn" data-comment-id="${data.id}"><i class="fa-solid fa-trash"></i></button>
                            </div>
                            <p class="comment-text">${escapeHtml(data.text)}</p>
                            <div class="comment-time">${data.created_at}</div>
                        </div>
                    `;
                    
                    commentList.appendChild(commentItem);
                    
                    // Animate trigger
                    setTimeout(() => {
                        commentItem.style.opacity = "1";
                        commentItem.style.transform = "translateY(0)";
                    }, 50);
                    
                    // Scroll to bottom
                    commentList.scrollTop = commentList.scrollHeight;
                }
                
                // Update post action counts
                const postCard = commentForm.closest(".post-card");
                if (postCard) {
                    const commentCountSpan = postCard.querySelector(".comments-count");
                    if (commentCountSpan) {
                        commentCountSpan.textContent = `${data.total_comments} Comment${data.total_comments !== 1 ? 's' : ''}`;
                    }
                }
                
                // Reset text field
                inputField.value = "";
            }
        } catch (error) {
            console.error("Error posting comment:", error);
        }
    });

    // 3. Delete Comment AJAX
    document.body.addEventListener("click", async (e) => {
        const deleteBtn = e.target.closest(".delete-comment-btn");
        if (!deleteBtn) return;
        
        e.preventDefault();
        const commentId = deleteBtn.dataset.commentId;
        const url = `/comment/${commentId}/delete/`;
        
        try {
            const response = await fetch(url, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrftoken,
                    "Content-Type": "application/json"
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                const commentItem = document.querySelector(`#comment-${commentId}`);
                if (commentItem) {
                    // Fade out animation
                    commentItem.style.opacity = "0";
                    commentItem.style.transform = "translateY(-10px)";
                    setTimeout(() => {
                        commentItem.remove();
                    }, 300);
                }
                
                // Update comments count on the post card
                const postCard = deleteBtn.closest(".post-card");
                if (postCard) {
                    const commentCountSpan = postCard.querySelector(".comments-count");
                    if (commentCountSpan) {
                        commentCountSpan.textContent = `${data.total_comments} Comment${data.total_comments !== 1 ? 's' : ''}`;
                    }
                }
            }
        } catch (error) {
            console.error("Error deleting comment:", error);
        }
    });

    // 4. Follow / Unfollow User AJAX
    document.body.addEventListener("click", async (e) => {
        const followBtn = e.target.closest(".btn-follow-toggle");
        if (!followBtn) return;
        
        e.preventDefault();
        const userId = followBtn.dataset.userId;
        const url = `/user/${userId}/follow/`;
        
        try {
            const response = await fetch(url, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrftoken,
                    "Content-Type": "application/json"
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                
                // Toggle styles across all follow buttons representing this user
                const relatedBtns = document.querySelectorAll(`.btn-follow-toggle[data-user-id="${userId}"]`);
                relatedBtns.forEach(btn => {
                    if (data.following) {
                        btn.className = "btn-neon btn-neon-blue btn-follow-toggle btn-follow-sm";
                        btn.innerHTML = `<i class="fa-solid fa-user-check"></i> Following`;
                    } else {
                        btn.className = "btn-neon btn-neon-purple btn-follow-toggle btn-follow-sm";
                        btn.innerHTML = `<i class="fa-solid fa-user-plus"></i> Follow`;
                    }
                });
                
                // Update profile stats if on user's profile page
                const followersVal = document.querySelector("#followers-stat-val");
                if (followersVal && data.followers_count !== undefined) {
                    followersVal.textContent = data.followers_count;
                }
                const followingVal = document.querySelector("#following-stat-val");
                if (followingVal && data.following_count !== undefined) {
                    followingVal.textContent = data.following_count;
                }
            }
        } catch (error) {
            console.error("Error following user:", error);
        }
    });

    // Simple HTML escaping helper for dynamically added text
    function escapeHtml(text) {
        return text
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }
});

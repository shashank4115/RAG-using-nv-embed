css = '''
<style>
.chat-message {
    padding: 0.5rem;
    border-radius: 0.3rem;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
}
.chat-message.user {
    background-color: #2b313e;
}
.chat-message.bot {
    background-color: #475063;
}
.chat-message .avatar {
    width: 30px;
    height: 30px;
    flex-shrink: 0;
}
.chat-message .avatar img {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    object-fit: cover;
}
.chat-message .message {
    width: calc(100% - 40px);
    padding: 0 0.5rem;
    color: #fff;
}
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://i.pinimg.com/originals/0c/67/5a/0c675a8e1061478d2b7b21b330093444.gif">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://static.vecteezy.com/system/resources/previews/005/544/718/non_2x/profile-icon-design-free-vector.jpg">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''
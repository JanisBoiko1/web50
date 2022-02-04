document.addEventListener('DOMContentLoaded', function() {
    // Use buttons to toggle between views
    document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
    document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
    document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
    document.querySelector('#compose').addEventListener('click', () => compose_email(0));

    //sending e-mails
    document.querySelector('form').onsubmit = function() {
            const recipients = document.querySelector('#compose-recipients').value
            const subject = document.querySelector('#compose-subject').value
            const body = document.querySelector('#compose-body').value

            //updating JSON with values from form
            fetch('/emails', {
                    method: 'POST',
                    body: JSON.stringify({
                        recipients: recipients,
                        subject: subject,
                        body: body
                    })
                })
                .then(response => response.json())
                .then(result => {
                    // Print result
                    console.log(result)
                })
                //loading sent mailbox
            load_mailbox('sent')
            return false

        }
        // By default, load the inbox
    load_mailbox('inbox');

});

//loading compose email form
function compose_email(id) {

    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';
    document.querySelector('#email-open').style.display = 'none';

    if (id === 0) {
        // Clear out composition fields if new email
        document.querySelector('#compose-subject').value = '';
        document.querySelector('#compose-body').value = '';
        document.querySelector('#compose-recipients').value = '';
    } else {
        //fetch email to be replied
        fetch(`/emails/${id}`)
            .then(response => response.json())
            .then(email => {
                // Print email
                console.log(email);

                //pre-fill subject, body and recipient lines
                document.querySelector('#compose-subject').value = `Re: ${email.subject}`
                document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: ${email.body}.`
                document.querySelector('#compose-recipients').value = email.sender;

            });
    }


}


function load_mailbox(mailbox) {

    // Show the mailbox and hide other views
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-open').style.display = 'none';

    //select part of the HTML were mailboxes will be shown
    const div = document.querySelector('#emails-view')
    let read = false

    // Show the mailbox name
    document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

    //fetch emails from mailbox
    fetch(`/emails/${mailbox}`)
        .then(response => response.json())
        .then(emails => {
            // Print emails
            console.log(emails);

            //define if email was or wasn't read
            for (let i = 0; i < emails.length; i++) {
                let email = emails[i]
                if (email.read == true) {
                    read = true
                } else {
                    read = false
                }

                //render each email in a different way according to mailbox
                if (mailbox == "inbox") {

                    div.innerHTML += `<div class="container" onclick="openEmail(${email.id}, ${mailbox})"> 
                    <div class="row" id="${read}-email-div">
                    <div class="col" id="email-sender">${email.sender}</div>
                    <div class="col-6">${email.subject}</div>
                    <div class="col" id="email-timestamp">${email.timestamp}</div>
                    </div>
                    </div>`
                } else if (mailbox == "sent") {

                    div.innerHTML += `<div class="container" onclick="openEmail(${email.id}, ${mailbox})"> 
                    <div class="row" id="${read}-email-div">
                    <div class="col" id="email-sender">${email.recipients}</div>
                    <div class="col-6">${email.subject}</div>
                    <div class="col" id="email-timestamp">${email.timestamp}</div>
                    </div>
                    </div>`
                } else if (mailbox == "archive") {

                    div.innerHTML += `<div class="container" onclick="openEmail(${email.id}, ${mailbox})"> 
                    <div class="row" id="${read}-email-div">
                    <div class="col" id="email-sender">${email.sender}</div>
                    <div class="col" id="email-sender">${email.recipients}</div>
                    <div class="col-5">${email.subject}</div>
                    <div class="col" id="email-timestamp">${email.timestamp}</div>
                    </div>`
                }

            }

        });

}

function openEmail(id, mailbox) {
    // Show the email-open and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-open').style.display = 'block';

    const emailDiv = document.querySelector('#email-open')

    fetch(`/emails/${id}`)
        .then(response => response.json())
        .then(email => {
            // Print email
            console.log(email);

            // Show the email’s sender, recipients, subject, timestamp, body and buttons
            // Buttons change according to mailbox
            if (mailbox.textContent == "Inbox") {

                emailDiv.innerHTML = `<hr>
                <div id="email-info">
                <p><b>From:</b> ${email.sender}</p>
                <p><b>To:</b> ${email.recipients}</p>
                <p><b>Subject:</b> ${email.subject}</p>
                <p><b>Timestamp:</b> ${email.timestamp}</p>
                <button id="reply" class="btn btn-outline-primary" onclick="compose_email(${email.id})">Reply</button>
                <button id="archive-btn" class="btn btn-outline-primary" onclick="archive(${email.id})">Archive</button>
                </div>
                <hr>
                <p>${email.body}</p>`

            } else if (mailbox.textContent == "Sent") {
                emailDiv.innerHTML = `<hr>
                <div id="email-info">
                <p><b>From:</b> ${email.sender}</p>
                <p><b>To:</b> ${email.recipients}</p>
                <p><b>Subject:</b> ${email.subject}</p>
                <p><b>Timestamp:</b> ${email.timestamp}</p>
                <button class="btn btn-outline-primary" id="reply" onclick="compose_email(${email.id})">Reply</button>
                </div>
                <hr>
                <p>${email.body}</p>`

            } else {
                emailDiv.innerHTML = `<hr>
                <div id="email-info">
                <p><b>From:</b> ${email.sender}</p>
                <p><b>To:</b> ${email.recipients}</p>
                <p><b>Subject:</b> ${email.subject}</p>
                <p><b>Timestamp:</b> ${email.timestamp}</p>
                <button class="btn btn-outline-primary" id="reply" onclick="compose_email(${email.id})">Reply</button>
                <button id="unarchive-btn" class="btn btn-outline-primary" onclick="unarchive(${email.id})">Unarchive</button>
                </div>
                <hr>
                <p>${email.body}</p>`

            }


        });

    // set email.read to true
    fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            read: true
        })
    })

}

//archive email
function archive(id) {

    // set email.archived to true
    fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: true
        })
    })

    //load inbox
    load_mailbox('inbox')
}

//unarchive email
function unarchive(id) {

    // set email.archived to false
    fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: false
        })
    })

    //load inbox
    load_mailbox('inbox')
}
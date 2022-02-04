document.addEventListener('DOMContentLoaded', function() {
    // Use buttons to toggle between views
    document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
    document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
    document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
    document.querySelector('#compose').addEventListener('click', () => compose_email(0));

    document.querySelector('form').onsubmit = function() {
            const recipients = document.querySelector('#compose-recipients').value
            const subject = document.querySelector('#compose-subject').value
            const body = document.querySelector('#compose-body').value

            //console.log(recipients)
            //console.log(subject)
            //console.log(body)

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
            load_mailbox('sent')
            return false

        }
        // By default, load the inbox
    load_mailbox('inbox');

});


function compose_email(id) {
    console.log(id)

    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';
    document.querySelector('#email-open').style.display = 'none';

    if (id === 0) {
        // Clear out composition fields
        document.querySelector('#compose-subject').value = '';
        document.querySelector('#compose-body').value = '';
        document.querySelector('#compose-recipients').value = '';
    } else {

        fetch(`/emails/${id}`)
            .then(response => response.json())
            .then(email => {
                // Print email
                console.log(email);
                document.querySelector('#compose-subject').value = `Re: ${email.subject}`
                    //"On Jan 1 2020, 12:00 AM foo@example.com wrote:"                
                document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: ${email.body}.`
                document.querySelector('#compose-recipients').value = email.sender;

            });
    }


}

// The load_mailbox function also takes an argument, 
// which will be the name of the mailbox that the user is trying to view. 
function load_mailbox(mailbox) {

    // Show the mailbox and hide other views
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-open').style.display = 'none';
    //console.log('you are in: ' + mailbox)

    const div = document.querySelector('#emails-view')
        //console.log(div)
    let read = false

    // Show the mailbox name
    document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

    fetch(`/emails/${mailbox}`)
        .then(response => response.json())
        .then(emails => {
            // Print emails
            console.log(emails);

            // ... do something else with emails ...
            for (let i = 0; i < emails.length; i++) {
                let email = emails[i]
                if (email.read == true) {
                    console.log("it was read")
                    read = true
                } else {
                    read = false
                }

                // Each email should then be rendered in its own box 
                // (e.g. as a <div> with a border) that displays who the
                // email is from, what the subject line is, and the 
                // timestamp of the email.

                if (mailbox == "inbox") {
                    //console.log("inbox")
                    div.innerHTML += `<div class="container" onclick="openEmail(${email.id}, ${mailbox})"> 
                    <div class="row" id="${read}-email-div">
                    <div class="col" id="email-sender">${email.sender}</div>
                    <div class="col-6">${email.subject}</div>
                    <div class="col" id="email-timestamp">${email.timestamp}</div>
                    </div>
                    </div>`
                } else if (mailbox == "sent") {
                    //console.log("sent")
                    div.innerHTML += `<div class="container" onclick="openEmail(${email.id}, ${mailbox})"> 
                    <div class="row" id="${read}-email-div">
                    <div class="col" id="email-sender">${email.recipients}</div>
                    <div class="col-6">${email.subject}</div>
                    <div class="col" id="email-timestamp">${email.timestamp}</div>
                    </div>
                    </div>`
                } else if (mailbox == "archive") {
                    //console.log("archived")
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
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-open').style.display = 'block';
    //console.log(id)
    let read = true
    let arr = []
    const emailDiv = document.querySelector('#email-open')
        //console.log(emailDiv)

    fetch(`/emails/${id}`)
        .then(response => response.json())
        .then(email => {
            // Print email
            console.log(email);
            for (let i = 0; i < email.recipients.length; i++) {
                arr.push(email.recipients[i])
                    //console.log(arr)
            }

            // Your application should show the email’s sender, recipients, subject, timestamp, and body.
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
    fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            read: true
        })
    })

}

function archive(id) {
    console.log("archive email " + id)
    fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: true
        })
    })

    //localStorage.clear()
    load_mailbox('inbox')
}

function unarchive(id) {
    console.log("unarchive email " + id)
    fetch(`/emails/${id}`, {
            method: 'PUT',
            body: JSON.stringify({
                archived: false
            })
        })
        //load_mailbox('inbox')
    load_mailbox('inbox')
}
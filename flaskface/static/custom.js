// Initialise Pusher
const pusher = new Pusher('ca7c12f18787cfa7312a', {
    cluster: 'ap2',
    ssl: true
});

var channel = pusher.subscribe('Blog');

channel.bind('new_comment', (data) => {
    console.log("the data is");
    $('#comm').append(`
            <h>${data.data.myComment}</h>

   `)
});


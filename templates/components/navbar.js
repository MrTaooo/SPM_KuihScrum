// I tried to use the url thingy to get the access right but it doesn't work
// const urlParams = new URLSearchParams(window.location.search);
// var rights = urlParams.get("rights");

const app = Vue.createApp({
})

app.component('navbar', {     
    data() {
        return {
            // accessRight: 0,
        } 
    },  
    // trying to pass assessRight value from app.vue to navbar.js
    props: ['access_right'],                   
    template: `<nav class="navbar navbar-expand-md navbar-dark nav-color">
                <div class="container">
                    <a class="navbar-brand text-white" href="#"><i class="bi bi-person-fill fs-1 profile-icon"></i> All in One </a>
                    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                    </button>
                    <div v-if="access_right === '1'" class="collapse navbar-collapse" id="navbarSupportedContent">
                        <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
                        <li class="nav-item">
                            <a class="nav-link" href="index.html">Apply</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" :href="'manage.html?rights=' + access_right">Manage</a>
                        </li>
                        </ul>
                    </div>
                </div>
            </nav>`
})

// commented out while fixing component
// const nav = app.mount('#navbar')
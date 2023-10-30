
// Navbar component
const Navbar = {
    props: ['access_right'],
    template: `<nav class="navbar navbar-expand-md navbar-dark nav-color">
      <div class="container">
        <a class="navbar-brand" href="index.html"><img src="./assets/allinone_logo.png" height="50"></a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div v-if="access_right === '1'" class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <a id="applyButton" class="nav-link" :href="'index.html?rights=' + access_right" :class="{ active: isActivePage('index.html') }">Apply</a>
            </li>
            <li class="nav-item">
              <a id="manageButton" class="nav-link" :href="'manage.html?rights=' + access_right" :class="{ active: isActivePage('manage.html') }">Manage</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>`,
    created: function () {
      this.highlightActivePage();
    },
    methods: {
      highlightActivePage: function () {
        const path = window.location.pathname;
        if (path.includes('index.html')) {
          localStorage.setItem('activePage', 'index.html');
        } else if (path.includes('manage.html')) {
          localStorage.setItem('activePage', 'manage.html');
        }
      },
      isActivePage: function (page) {
        return localStorage.getItem('activePage') === page;
      },
    },
  };
  
  export default Navbar;
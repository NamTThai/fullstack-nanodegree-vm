document.addEventListener("WebComponentsReady", function() {
  var eventListener = document.querySelector("#eventListener");

  // When user click on a button to add new pokemon. Verify whether user has
  // signed in. If he/she signed in, opens Add Pokemon dialog; otherwise,
  // request user to sign in
  eventListener.eAddPokemon = function() {
    var gSignin = document.querySelector("google-signin");
    var dialog = document.querySelector("pokemon-info");
    if (gSignin.signedIn) {
      dialog.selected = "add";
      var currentSection = document.querySelector("#typeSection").selected;
      if (currentSection != "latest_item") {
        dialog.defaultType = currentSection;
      }
    } else {
      dialog.selected = "signin";
    }
    dialog.open();
  };

  // Display the correct section when user clicks on left drawer panel
  eventListener.eDrawerItemClick = function(event) {
    var drawer = document.querySelector(".drawer-panel");
    if (drawer.narrow) {
      drawer.closeDrawer();
    }

    var route = event.target.innerHTML.trim();
    window.history.pushState("", "", route);

    var ironPage = document.querySelector('iron-pages');
    ironPage.select(route);
  };

  // Minimize header as user scroll down
  eventListener.eHeaderTransform = function(event) {
    var appName = document.querySelector('#mainToolbar .app-name');
    var middleContainer = document.querySelector('#mainToolbar .middle-container');
    var bottomContainer = document.querySelector('#mainToolbar .bottom-container');
    var heightDiff = event.detail.height - event.detail.condensedHeight;
    var yRatio = Math.min(1, event.detail.y / heightDiff);
    var maxMiddleScale = 0.50;
    var scaleMiddle = Math.max(maxMiddleScale, (heightDiff - event.detail.y) / (heightDiff / (1 - maxMiddleScale)) + maxMiddleScale);
    var scaleBottom = 1 - yRatio;

    Polymer.Base.transform('translate3d(0,' + yRatio * 100 + '%,0)', middleContainer);
    Polymer.Base.transform('scale(' + scaleBottom + ') translateZ(0)', bottomContainer);
    Polymer.Base.transform('scale(' + scaleMiddle + ') translateZ(0)', appName);
  };

  // Open signin dialog when user clicks on signin button
  eventListener.eLogin = function() {
    var dialog = document.querySelector("pokemon-info");
    dialog.selected = "signin";
    dialog.open();
  };

  // Open Pokemon info dialog when user clicks on Pokedex entry
  eventListener.eShowPokemon = function(event) {
    var pokemonId = $(event.target).closest("tr").attr("pokemon-id");
    var dialog = document.querySelector("pokemon-info");
    var user_email = null;
    if (document.querySelector("google-signin").signedIn) {
      user_email = gapi.auth2.getAuthInstance().currentUser.get().zt.po;
    }
    $.ajax("/v1/pokemon", {
      method: "GET",
      data: {
        id: pokemonId,
        user_email: user_email
      },

      success: function(data) {
        dialog.selected = "info";
        dialog.authorized = data.authorized;
        dialog.pokemon = data.pokemon;
        dialog.open();
      },

      error: function(error) {
        dialog.selected = "error";
        dialog.error = "Nothing found";
        dialog.open();
      }
    });
  };
});

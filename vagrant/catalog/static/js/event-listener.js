document.addEventListener("WebComponentsReady", function() {
  var eventListener = document.querySelector("#eventListener");

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

  eventListener.eLogin = function() {
    var dialog = document.querySelector("pokemon-info");
    dialog.selected = "signin";
    dialog.open();
  };

  eventListener.eShowPokemon = function(event) {
    var pokemonId = $(event.target).closest("tr").attr("pokemon-id");
    var dialog = document.querySelector("pokemon-info");
    $.ajax("/v1/pokemon", {
      method: "GET",
      data: {
        id: pokemonId
      },

      success: function(data) {
        dialog.selected = "info";
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

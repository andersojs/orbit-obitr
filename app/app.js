(function () {
  "use strict";

  angular
    .module("orbitrApp", [])
    .service("RsoService", [
      "$http",
      function ($http) {
        this.fetchAll = function () {
          return $http.get("/api/rso").then(function (response) {
            return response.data;
          });
        };

        this.fetchCatalog = function () {
          return $http.get("/api/rso/almanac/catalog").then(function (response) {
            return response.data;
          });
        };
      },
    ])
    .controller("MainController", [
      "$scope",
      "RsoService",
      function ($scope, RsoService) {
        var vm = this;
        vm.viewMode = "3d";
        vm.rsos = [];
        vm.catalogSize = 0;
        vm.filterText = "";
        vm.selectedRso = null;

        var viewer = null;
        var entityIndex = {};

        vm.filteredRsos = function () {
          if (!vm.filterText) {
            return vm.rsos;
          }
          var query = vm.filterText.toLowerCase();
          return vm.rsos.filter(function (rso) {
            var aliasMatch = (rso.aliases || []).some(function (alias) {
              return alias.toLowerCase().indexOf(query) >= 0;
            });
            var tagMatch = (rso.tags || []).some(function (tag) {
              return tag.toLowerCase().indexOf(query) >= 0;
            });
            return (
              (rso.display_name || "").toLowerCase().indexOf(query) >= 0 ||
              (rso.international_designator || "").toLowerCase().indexOf(query) >= 0 ||
              (String(rso.satcat_number) || "").toLowerCase().indexOf(query) >= 0 ||
              aliasMatch ||
              tagMatch
            );
          });
        };

        vm.focusRso = function (rso) {
          vm.selectedRso = rso;
          highlightEntity(rso);
        };

        vm.changeView = function (mode) {
          vm.viewMode = mode;
          if (!viewer) {
            return;
          }
          if (mode === "2d") {
            viewer.scene.morphTo2D(0.8);
          } else {
            viewer.scene.morphTo3D(0.8);
          }
        };

        function init() {
          initCesium();
          loadData();
        }

        function loadData() {
          RsoService.fetchCatalog().then(function (catalog) {
            vm.catalogSize = catalog.length;
          });

          RsoService.fetchAll().then(function (data) {
            vm.rsos = data;
            vm.selectedRso = data.length ? data[0] : null;
            plotEntities();
          });
        }

        function initCesium() {
          if (viewer || typeof Cesium === "undefined") {
            return;
          }
          viewer = new Cesium.Viewer("cesiumContainer", {
            imageryProvider: new Cesium.UrlTemplateImageryProvider({
              url: "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
              credit: "© OpenStreetMap contributors",
            }),
            timeline: false,
            animation: false,
            geocoder: false,
            sceneMode: Cesium.SceneMode.SCENE3D,
            terrainProvider: new Cesium.EllipsoidTerrainProvider(),
            baseLayerPicker: false,
            sceneModePicker: false,
            navigationHelpButton: false,
          });
          viewer.scene.globe.enableLighting = true;
        }

        function plotEntities() {
          if (!viewer) {
            return;
          }
          viewer.entities.removeAll();
          entityIndex = {};

          vm.rsos.forEach(function (rso) {
            var coords = pseudoCoordinates(rso.satcat_number);
            var entity = viewer.entities.add({
              name: rso.display_name,
              position: Cesium.Cartesian3.fromDegrees(coords.lon, coords.lat, coords.alt),
              point: {
                pixelSize: 8,
                color: Cesium.Color.CYAN,
                outlineColor: Cesium.Color.BLACK,
                outlineWidth: 1,
              },
              description:
                "<strong>" +
                rso.display_name +
                "</strong><br/>SatCat " +
                rso.satcat_number +
                "<br/>" +
                rso.international_designator,
            });
            entityIndex[rso.satcat_number] = entity;
          });

          if (vm.selectedRso) {
            highlightEntity(vm.selectedRso);
          }
        }

        function highlightEntity(rso) {
          if (!viewer || !rso) {
            return;
          }
          var entity = entityIndex[rso.satcat_number];
          if (entity) {
            viewer.selectedEntity = entity;
            viewer.flyTo(entity, {
              duration: 1.2,
            });
          }
        }

        function pseudoCoordinates(input) {
          var seed = 0;
          var text = String(input || "");
          for (var i = 0; i < text.length; i += 1) {
            seed += text.charCodeAt(i) * (i + 1);
          }
          var lat = (seed % 180) - 90;
          var lon = ((seed * 7) % 360) - 180;
          var altitude = 20000000 + (seed % 5000000);
          return { lat: lat, lon: lon, alt: altitude };
        }

        $scope.$watch(
          function () {
            return vm.rsos.length;
          },
          function () {
            plotEntities();
          }
        );

        init();
      },
    ]);
})();

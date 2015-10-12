<%
    root = h.url_for( "/" )
    app_root = root + "plugins/visualizations/csg/static/"
%>

<!DOCTYPE HTML>
<html>
    <head>
        <!-- CSG Viewer is a web application for 3D shape visualization. -->
        <title>${hda.name} | ${visualization_name}</title>

        ${h.javascript_link( app_root + 'dat.gui.min.js' )}
        ${h.javascript_link( app_root + 'three.min.js' )}
        ${h.javascript_link( app_root + 'OrbitControls.js' )}
        ${h.javascript_link( app_root + 'PLYLoader.js' )}
        ${h.javascript_link( app_root + 'VTKLoader.js' )}
    </head>
    <body>
        <!-- Div which will hold the Output -->
        <div id="WebGL-output"></div>

        <script type="text/javascript">

            // Global variables
            var container;
            var scene;
            var camera;
            var renderer;
            var controls;
            var bbHelper;
            var defaultBackgroundColor = 0x4d576b;

            init();
            //animate();

            function init() {
                window.addEventListener('resize', onWindowResize, false);

                // Scene
                scene = new THREE.Scene();
                // Color, near, far
               scene.fog = new THREE.Fog(0x111111, 0.1, 1000);

                // Data format and loader
                var hdaExt  = '${hda.ext}';
                if (hdaExt == 'plyascii' || hdaExt == 'plybinary') {
                    // This returns THREE.Geometry()
                    var loader = new THREE.PLYLoader();
                } else {
                    // This returns THREE.BufferGeometry()
                    var loader = new THREE.VTKLoader();
                }

                loader.load("${h.url_for( controller='/datasets', action='index')}/${trans.security.encode_id( hda.id )}/display",
                function (geometry) {

                    var surface = new THREE.MeshPhongMaterial({shading: THREE.SmoothShading,
                                                                side: THREE.DoubleSide,
                                                                shininess: 100,
                                                                emissive: 0x000000,
                                                                specular: 0x111111,
                                                                metal: false});

                    var edges = new THREE.MeshBasicMaterial({color: 0x111111, 
                                                             wireframe: true,
                                                             wireframeLinewidth: 2});

                    geometry.receiveShadow = true;
                    geometry.computeFaceNormals();

                    // Normals may or may not have been set
                    if ( ! geometry.getAttribute( 'normal' ) ) {

                         geometry.computeVertexNormals();

                    }

                    var geometryHasColor = false;
                    if ( geometry.type == "BufferGeometry" && 
                         geometry.getAttribute( 'color' ) ) {

                        geometryHasColor = true;

                        // Color vertices
                        surface[ 'vertexColors' ] = THREE.VertexColors;

                    } else {

                        // No color, use gui input
                        surface[ 'color' ] = new THREE.Color( 0xAAAAAA );

                    }

                    var meshSurface = new THREE.Mesh(geometry, surface);
                    scene.add(meshSurface);

                    var meshEdges = new THREE.Mesh(geometry, edges);
                    // will be added on request to the scene

                    // Define the BoundingBox
                    bbHelper = new THREE.BoundingBoxHelper(meshSurface, 0xff0000);
                    bbHelper.update();

                    // Determine box boundaries based on geometry.
                    var xmin = bbHelper.box.min.x;
                    var xmax = bbHelper.box.max.x;
                    var xmid = 0.5*(xmin + xmax);
                    var xlen = xmax - xmin;

                    var ymin = bbHelper.box.min.y;
                    var ymax = bbHelper.box.max.y;
                    var ymid = 0.5*(ymin + ymax);
                    var ylen = ymax - ymin;

                    var zmin = bbHelper.box.min.z;
                    var zmax = bbHelper.box.max.z;
                    var zmid = 0.5*(zmin + zmax);
                    var zlen = zmax - zmin;

                    var lightX = xmid + 1*xlen;
                    var lightY = ymid + 2*ylen;
                    var lightZ = zmid + 5*zlen;

                    // Get the center of the shape
                    var shapeWidth = ( xmin > xmax ) ? xmin - xmax : xmax - xmin;
                    var shapeHeight = ( ymin > ymax ) ? ymin - ymax : ymax - ymin;
                    var shapeDepth = ( zmin > zmax ) ? zmin - zmax : zmax - zmin;

                    var centroidX = xmin + ( shapeWidth / 2 ) + meshSurface.position.x;
                    var centroidY = ymin + ( shapeHeight / 2 )+ meshSurface.position.y;
                    var centroidZ = zmin + ( shapeDepth / 2 ) + meshSurface.position.z;

                    meshSurface.geometry.centroid = { x : centroidX, y : centroidY, z : centroidZ };

                    // Camera
                    var SCREEN_WIDTH = window.innerWidth;
                    var SCREEN_HEIGHT = window.innerHeight;
                    var VIEW_ANGLE = 45;
                    var ASPECT = SCREEN_WIDTH / SCREEN_HEIGHT;
                    var NEAR = 1;
                    var FAR = 10000;
                    camera = new THREE.PerspectiveCamera(VIEW_ANGLE, ASPECT, NEAR, FAR);
                    camera.position.x = xmax + 5;
                    camera.position.y = ymax + 5;
                    camera.position.z = zmax + 5;

                    // Renderer
                    renderer = new THREE.WebGLRenderer({antialias: false});
                    renderer.shadowMapEnabled = true;
                    renderer.setClearColor(new THREE.Color(defaultBackgroundColor, 1.0));
                    renderer.setSize(SCREEN_WIDTH, SCREEN_HEIGHT);

                    // add the output of the renderer to the html element
                    container = document.getElementById("WebGL-output")
                    container.appendChild(renderer.domElement);

                    // Controls
                    controls = new THREE.OrbitControls(camera, renderer.domElement);

                    // Light
                    var light = new THREE.SpotLight(0xBBBBBB);
                    light.castShadow = true;
                    light.position.set(xmid + 5*xlen, ymid + 5*ylen, zmid + 5*zlen);
                    light.target.position.set(xmid, ymid, zmid);
                    light.exponent = 1;
                    light.angle = 60 * Math.PI / 180;
                    scene.add( light );
  
                    // Ambient light
                    var lightAmbient = new THREE.AmbientLight(0xffffff);
                    scene.add(lightAmbient);

                    // Axes
                    var origin = new THREE.Vector3(xmin, ymin, zmin);
                    var ex = new THREE.Vector3(xmax, 0, 0);
                    var ey = new THREE.Vector3(0, ymax, 0);
                    var ez = new THREE.Vector3(0, 0, zmax);
                    var xAxis = new THREE.ArrowHelper(ex, origin, xlen, 0xff0000);
                    var yAxis = new THREE.ArrowHelper(ey, origin, ylen, 0x00ff00);
                    var zAxis = new THREE.ArrowHelper(ez, origin, zlen, 0x0000ff);
                    scene.add(xAxis);
                    scene.add(yAxis);
                    scene.add(zAxis);

                    // GUI
                    gui = new dat.GUI();
                    parameters = {'background': '#4d576b',
                                  'shininess': 100,
                                  'color': '#aaaaaa',
                                  'emissive': '#000000',
                                  'specular': '#111111',
                                  'wireframe': false,
                                  'lightX': lightX,
                                  'lightY': lightY,
                                  'lightZ': lightZ};

                    var sceneFolder = gui.addFolder('scene');
                    
                    var backgroundGui = sceneFolder.addColor(parameters, 'background').name('background').listen();
                    backgroundGui.onChange( function(value) {renderer.setClearColor(value);} );

                    var materialFolder = gui.addFolder('material');

                    var materialShininessGui = materialFolder.add(parameters, 'shininess').min(0).max(100).step(5).listen();
                    materialShininessGui.onChange( function(value) {surface.shininess = value} );

                    if (! geometryHasColor) {
                        var materialColorGui = materialFolder.addColor(parameters, 'color').name('ambient color').listen();
                        materialColorGui.onChange( function(value) {surface.color.setHex(value.replace('#', '0x'));} );
                    }

                    var materialEmissiveGui = materialFolder.addColor(parameters, 'emissive').name('emissive color').listen();
                    materialEmissiveGui.onChange( function(value) {surface.emissive.setHex(value.replace('#', '0x'));} );

                    var materialSpecularGui = materialFolder.addColor(parameters, 'specular').name('specular color').listen();
                    materialSpecularGui.onChange( function(value) {surface.specular.setHex(value.replace('#', '0x'));} );

                    var materialEdgesGui = materialFolder.add(parameters, 'wireframe').listen();
                    materialEdgesGui.onChange( function(value) {if (value) {scene.add(meshEdges);} else {scene.remove(meshEdges);} } );

                    var lightsFolder = gui.addFolder('lights');

                    var lightXGui = lightsFolder.add(parameters, 'lightX' ).min(xmid-10*xlen).max(xmid+10*xlen).step(xlen/10.).name('x').listen();
                    lightXGui.onChange( function(value) {light.position.x = value} );

                    var lightYGui = lightsFolder.add(parameters, 'lightY' ).min(ymid-10*ylen).max(ymid+10*ylen).step(ylen/10.).name('y').listen();
                    lightYGui.onChange( function(value) {light.position.y = value} );

                    var lightZGui = lightsFolder.add(parameters, 'lightZ' ).min(zmid-10*zlen).max(zmid+10*zlen).step(zlen/10.).name('z').listen();
                    lightZGui.onChange( function(value) {light.position.z = value} );

                    // Animate
                    animate();
                });
            }

             function animate() {
               requestAnimationFrame(animate);
               render();
               controls.update();
             }

            function render() {
                renderer.render(scene, camera);
            }
 
            function onWindowResize() {
                camera.aspect = window.innerWidth / window.innerHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(window.innerWidth, window.innerHeight);
                controls.handleResize();
                render();
            }
        </script>
    </body>
</html>

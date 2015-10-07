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

            init();
            //animate();

            function init() {
                window.addEventListener('resize', onWindowResize, false);

                // Scene
                scene = new THREE.Scene();
                scene.fog = new THREE.Fog(0x808080, 2000, 4000);

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

                    var material = new THREE.MeshPhongMaterial({shading: THREE.SmoothShading,
                                                                side: THREE.DoubleSide,
                                                                shininess: 100});
                    geometry.receiveShadow = true;
                    geometry.computeFaceNormals();

                    // Normals may or may not have been set
                    if ( ! geometry.getAttribute( 'normal' ) ) {

                         geometry.computeVertexNormals();

                    }

                    if ( geometry.type == "BufferGeometry" && 
                         geometry.getAttribute( 'color' ) ) {

                        // Color vertices
                        material[ 'vertexColors' ] = THREE.VertexColors;

                    } else {

                        // No color, use some grey shade
                        material[ 'color' ] = new THREE.Color( 0xAAAAAA );

                    }

                    var mesh = new THREE.Mesh(geometry, material);
                    scene.add(mesh);

                    // Define the BoundingBox
                    bbHelper = new THREE.BoundingBoxHelper(mesh, 0xff0000);
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

                    var centroidX = xmin + ( shapeWidth / 2 ) + mesh.position.x;
                    var centroidY = ymin + ( shapeHeight / 2 )+ mesh.position.y;
                    var centroidZ = zmin + ( shapeDepth / 2 ) + mesh.position.z;

                    mesh.geometry.centroid = { x : centroidX, y : centroidY, z : centroidZ };

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
                    renderer.setClearColor(new THREE.Color(0x000000, 1.0));
                    renderer.setSize(SCREEN_WIDTH, SCREEN_HEIGHT);

                    // add the output of the renderer to the html element
                    container = document.getElementById("WebGL-output")
                    container.appendChild(renderer.domElement);

                    // Controls
                    controls = new THREE.OrbitControls(camera, renderer.domElement);

                    // Light
                    var light = new THREE.SpotLight( 0xBBBBBB );
                    light.castShadow = true;
                    light.position.set(xmid + 5*xlen, ymid + 5*ylen, zmid + 5*zlen);
                    light.target.position.set(xmid, ymid, zmid);
                    light.exponent = 1;
                    light.angle = 60 * Math.PI / 180;
                    scene.add( light );
  
                    // Ambient light
                    var lightAmbient = new THREE.AmbientLight( 0xffffff );
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
                    parameters = {'shininess': 100,
                                  'lightX': lightX,
                                  'lightY': lightY,
                                  'lightZ': lightZ}

                    var isoShininess = gui.add(parameters, 'shininess').min(0).max(100).step(2).name('shininess').listen();
                    isoShininess.onChange( function(value) {material.shininess = value} );

                    lightPositionFolder = gui.addFolder('light position');
                    lightXGui = lightPositionFolder.add(parameters, 'lightX' ).min(xmid-10*xlen).max(xmid+10*xlen).step(xlen/10.).listen();
                    lightXGui.onChange( function(value) {light.position.x = value} );

                    lightYGui = lightPositionFolder.add(parameters, 'lightY' ).min(ymid-10*ylen).max(ymid+10*ylen).step(ylen/10.).listen();
                    lightYGui.onChange( function(value) {light.position.y = value} );

                    lightZGui = lightPositionFolder.add(parameters, 'lightZ' ).min(zmid-10*zlen).max(zmid+10*zlen).step(zlen/10.).listen();
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

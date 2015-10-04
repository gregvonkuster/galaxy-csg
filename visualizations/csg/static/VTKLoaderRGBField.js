/**
 * @author mrdoob / http://mrdoob.com/ and Alex Pletzer
 */

THREE.VTKLoaderRGBField = function ( manager ) {

	this.manager = ( manager !== undefined ) ? manager : THREE.DefaultLoadingManager;

};

THREE.VTKLoaderRGBField.prototype = {

	constructor: THREE.VTKLoaderRGBField,

	load: function ( url, onLoad, onProgress, onError ) {

		var scope = this;

		var loader = new THREE.XHRLoader( scope.manager );
		loader.setCrossOrigin( this.crossOrigin );
		loader.load( url, function ( text ) {

			onLoad( scope.parse( text ) );

		}, onProgress, onError );

	},

	setCrossOrigin: function ( value ) {

		this.crossOrigin = value;

	},

	parse: function ( data ) {

		// connectivity of the triangles
		var indices = [];
		
		// triangles vertices
		var positions = [];
		
		// scalar field container
		var field = {};
		
		var fieldName = "";
		var fieldStagger = "";
		var result;
		
		// pattern for reading vertices
		var pat3Floats = /(\-?\d+\.?[\d\-\+e]*)\s+(\-?\d+\.?[\d\-\+e]*)\s+(\-?\d+\.?[\d\-\+e]*)/g;
		
		// pattern for connectivity
		var patConnectivity = /^(\d+)\s+([\s\d]*)/;
		
		// pattern for reading scalar field values
		var patInt = /(\d+)/g;
		
		// starts with a number
		var patNum = /^[ ]*\d+/;
		
		// indicates start of vertex data section
		var patPOINTS = /^POINTS /;
		
		// indicates start of polygon connectivity section 
		var patPOLYGONS = /^POLYGONS /;
		
		// POINT_DATA number_of_values 
		var patPOINT_DATA = /^POINT_DATA[ ]+(\d+)/;
		
		// CELL_DATA number_of_polys
		var patCELL_DATA = /^CELL_DATA[ ]+(\d+)/;
		
		// Field name number_of_fields
		var patFIELD = /^FIELD[ ]+([\w\_]+)\s+(\d+)/;
		
		// field_name num_components num_elements type
		var patFieldName = /^([a-zA-Z][\w\_]+)\s+(\d+)\s+(\d+)\s+(\w+)/;
		
		var inPointsSection = false;
		var inPolygonsSection = false;
		var inPointDataSection = false;
		var inCellDataSection = false;
		var inPointDataSection = false;
		var inFieldSection = false;
		var readData = false;
		var fieldCounter = 0;
		var numFields = 0;		

		var lines = data.split('\n');
		for ( var i = 0; i < lines.length; ++i ) {

			line = lines[i];

			if ( inPointsSection ) {

				// get the vertices

				while ( ( result = pat3Floats.exec( line ) ) !== null ) {
					var x = parseFloat( result[ 1 ] );
					var y = parseFloat( result[ 2 ] );
					var z = parseFloat( result[ 3 ] );
					positions.push( x, y, z );
				}
			}
			else if ( inPolygonsSection ) {
			
				if ( ( result = patConnectivity.exec( line ) ) !== null ) {
				
					// numVertices i0 i1 i2 ...
					var numVertices = parseInt( result[ 1 ] );
					var inds = result[ 2 ].split(/\s+/); 
					if ( numVertices >= 3 ) {
					    var i0 = parseInt( inds[ 0 ] );
					    var i1, i2;
					    var k = 1;
					    // split the polygon in numVertices - 2 triangles
						for ( var j = 0; j < numVertices - 2; ++j ) {
							i1 = parseInt( inds[ k ] );
							i2 = parseInt( inds[ k  + 1 ] );
						  	indices.push( i0, i1, i2 );
							k++;
						}
					}
				}
			}
			else if (  readData && ( inPointDataSection || inCellDataSection ) && 
			           ( patNum.exec(line) !== null ) && 
			           fieldStagger != "" && fieldName != "" ) {
			
				// read field values
			
				while ( ( result = patInt.exec( line ) ) !== null ) {
				
					field[ fieldStagger ][ fieldName ].push( parseInt( result[ 1 ] ) );
					
				}
			}
			else if ( fieldStagger != "" && ( result = patFieldName.exec( line ) ) !== null ) {
			
			
			  	// get the field name 

			    fieldName = result[ 1 ];
			    field[ fieldStagger ][ fieldName ] = [];
			    readData = true;
			}

			if ( patPOLYGONS.exec( line ) !== null ) {
				inPolygonsSection = true;
				inPointsSection = false;
				inPointDataSection = false;
				inCellDataSection = false;
			}
			else if ( patPOINTS.exec( line ) !== null ) {
				inPolygonsSection = false;
				inPointsSection = true;
				inPointDataSection = false;
				inCellDataSection = false;
			}
			else if ( patFIELD.exec( line ) !== null ) {
				readData = false;
			}
			else if ( ( result = patPOINT_DATA.exec( line ) ) !== null ) {
			
			    // new point data section 
			    			    			    
				inPolygonsSection = false;
				inPointsSection = false;
				inPointDataSection = true;
				inCellDataSection = false;
				fieldStagger = "point";
				field[ fieldStagger ] = {};
			}
			else if ( ( result = patCELL_DATA.exec( line ) ) !== null ) {
			
				// new cell data section 
							    
				inPolygonsSection = false;
				inPointsSection = false;
				inPointDataSection = false;
				inCellDataSection = true;
				fieldStagger = "cell";
				field[ fieldStagger ] = {};
				
			}
		}

		var geometry = new THREE.BufferGeometry();
		geometry.addAttribute( 'index', new THREE.BufferAttribute( new ( indices.length > 65535 ? Uint32Array : Uint16Array )( indices ), 1 ) );
		geometry.addAttribute( 'position', new THREE.BufferAttribute( new Float32Array( positions ), 3 ) );
				
		if ( field.hasOwnProperty( 'point' ) ) {

		     var pf = field[ 'point' ];
		     if ( pf.hasOwnProperty( 'red' ) && pf.hasOwnProperty( 'green' ) && pf.hasOwnProperty( 'blue' ) ) {
				colorArray = [];
				var r = pf[ 'red' ];
				var g = pf[ 'green' ];
				var b = pf[ 'blue' ];
				for (var i = 0; i < r.length; ++i) {
					colorArray.push( r[ i ]/255., g[ i ]/255., b[ i ]/255. );
				}
				geometry.addAttribute( 'color', 
				                       new THREE.BufferAttribute( 
				                                new Float32Array( colorArray ), 3 
				                                                ) 
				                     );
			}
		}
		
		return geometry;

	}

};

THREE.EventDispatcher.prototype.apply( THREE.VTKLoaderRGBField.prototype );

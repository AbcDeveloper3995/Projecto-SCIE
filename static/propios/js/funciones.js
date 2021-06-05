//--------------------------------------------------------INICIALIZACIONES----------------------------------------------------------//
 $('#dataTable').dataTable({});

 $('.select2').select2({
     theme: 'bootstrap4',
     language: 'es',
     placeholder: 'Seleccione una opcion'
 });

new WOW().init();


new tippy('.miTippy', {
    animation: 'perspective',
});

//-------------------------------------PROCEDIMIENTO PARA ACTUALIZAR EN TIEMPO REAL LOS DATOS EN LAS TABLAS--------------------//

const tabla = (nombreSeccion, idSeccion) => {
     let nombre_seccion = "table"+nombreSeccion;
     let form_verificacion = $('.formVerificacion')
    let datatable = $('.'+nombre_seccion).DataTable({
        deferRender: true,
        destroy:true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'mostrarInstancias',
                'id_seccion':idSeccion,
            },
            dataSrc: ""
        },
        columns: [
            {"data": "codigo_id"},
            {"data": "columna_id"},
            {"data": "modelo_1"},
            {"data": "registro_1"},
            {"data": "diferencia_1"},
            {"data": "modelo_2"},
            {"data": "registro_1"},
            {"data": "diferencia_2"},
            {"data": "modelo_3"},
            {"data": "registro_3"},
            {"data": "diferencia_3"},
        ],
        initComplete: function (settings, json) {

        }
    });
    if (datatable.flatten().Length === 0) {
        alert('Empty table1');
    } else {
        for(var i=0; i<form_verificacion.length; i++){
            if(idSeccion === parseInt(form_verificacion[i].dataset.id)){
                form_verificacion.prop('hidden', false);
                return false;
            }
        }
    }

};



//--------------------------------------------------------VALIDACIONES DE FECHAS------------------------------------------------//

 $('.date').datetimepicker({
        format: 'DD/MM/YYYY',
        date:moment().format("YYYY-MM-DD"),
        locale:'es',
        maxDate:moment().format("YYYY-MM-DD"),
    });


//--------------------------------------VALIDACIONES PARA EL FORM INSTANCIAS---------------------------------------------//

const validate_no_empty_instancias = (seccionForm, seccionCampo) => {
for (var i=0;i,i<seccionCampo.length; i++){
        if (seccionForm === seccionCampo[i].dataset.seccion && seccionCampo[i].value === "") {
              toastr.error("Asegurese de no dejar campos vacios.", 'Error', {
             progressBar: true,
             closeButton: true,
             "timeOut": "5000",
    });
              return false
        }
    }
}

//-----------------------VALIDACIONES DEL FORM VERIFICACION-------------------------------------------//

const validate_indicadores_no_empty = (seccion_form_verificacion, campo) => {
    for (var i=0;i,i<campo.length; i++){
        if (seccion_form_verificacion === campo[i].dataset.seccion && campo[i].value === "") {
              toastr.error("Asegurese de no dejar campos vacios.", 'Error', {
             progressBar: true,
             closeButton: true,
             "timeOut": "5000",
    });
              return false
        }
    }
}

const validate_indicadores_positivos = (seccion_form_verificacion, campo) => {
    for (var i=0;i,i<campo.length; i++){
        if (seccion_form_verificacion === campo[i].dataset.seccion && campo[i].value < 0) {
              toastr.error("No se admiten valores negativos.", 'Error', {
             progressBar: true,
             closeButton: true,
             "timeOut": "5000",
    });
              return false
        }
    }
}

const validate_dependencia_indicadore = (seccion_form_verificacion, listaIndVerificados, listaIndCoinciden) => {
    for (var i=0; i<listaIndVerificados.length; i++){
        if (seccion_form_verificacion === listaIndVerificados[i].dataset.seccion) {
              for (var j=0; j<listaIndCoinciden.length; j++){
        if (seccion_form_verificacion === listaIndCoinciden[j].dataset.seccion && parseInt(listaIndVerificados[i].value) < parseInt(listaIndCoinciden[j].value )) {
              toastr.error("La cantidad de indicadores que coinciden no puede ser mayor que la cantidad de verificados.", 'Error', {
             progressBar: true,
             closeButton: true,
             "timeOut": "5000",
    });
              return false
        }
    }

        }
    }
}



//-------------------------PROCEDIMIENTO PARA GUARDAR LO VERIFICADO-------------------------------------//

$('form[name="formVerificacion"]').on('submit', function (e) {
    e.preventDefault();
    let seccion_form_verificacion = $(this).data('seccion');
    let listaIndVerificados = $('input[name="indicadoresVerificados"]');
    let listaIndCoinciden = $('input[name="indicadoresCoinciden"]');
    let listaIndIncluidos = $('select[name="indicadoresIncluidos"]');
    let id_seccion = $(this).data('id');

    if(validate_indicadores_no_empty(seccion_form_verificacion, listaIndVerificados) === false){return false};
    if(validate_indicadores_no_empty(seccion_form_verificacion, listaIndCoinciden) === false){return false};
    if(validate_indicadores_no_empty(seccion_form_verificacion, listaIndIncluidos) === false){return false};
    if(validate_indicadores_positivos(seccion_form_verificacion, listaIndVerificados) === false){return false};
    if(validate_indicadores_positivos(seccion_form_verificacion, listaIndCoinciden) === false){return false};
    if(validate_dependencia_indicadore(seccion_form_verificacion, listaIndVerificados, listaIndCoinciden) === false){return false};

    let  campos = new FormData(this);

      campos.forEach(function (value, key) {
         console.log(key+' : '+value)
     });
    $.ajax({
        url: '/seccion/comprobacionInd/'+id_seccion+'/',
        type: 'POST',
        data: campos,
        dataType: 'json',
        processData: false,
        contentType: false
    }).done(function (data) {
          toastr.success(data.exito, 'Exito', {
             progressBar: true,
             closeButton: true,
             "timeOut": "5000",
    });
    }).fail(function (jqXHR, textStatus, errorThrown) {
        alert(textStatus + ' : ' + errorThrown)
    })
});

//-----------------------VALIDACIONES PARA LA SECCION IDENTIFICACION Y SOBRE ENTIDAD-----------------------------------------//
const verificarExistencia = (element) => {
    if(element.length==0){
        return false
    }
}

const validacionChecked = (element) => {
    if(element.is(':checked')){
         console.log('chekeado')
     }else {
         toastr.error(element.prop('name')+" es requerido.", 'Error', {
             progressBar: true,
             closeButton: true,
             "timeOut": "5000",
    });
         return false;
     }
}

const validate_radios_no_empty = () => {
    let cod_pregunta_11 =  $('.formCaptacion input[data-cod-pregunta="11"]' );
    let cod_pregunta_13 =  $('.formCaptacion input[data-cod-pregunta="13"]' );
    let cod_pregunta_14 =  $('.formCaptacion input[data-cod-pregunta="14"]' );
    let cod_pregunta_15 =  $('.formCaptacion input[data-cod-pregunta="15"]' );
    let cod_pregunta_21 =  $('.formCaptacion input[data-cod-pregunta="21"]' );
    let cod_pregunta_22 =  $('.formCaptacion input[data-cod-pregunta="22"]' );
    let cod_pregunta_41 =  $('.formCaptacion input[data-cod-pregunta="41"]' );
    let cod_pregunta_51 =  $('.formCaptacion input[data-cod-pregunta="51"]' );
    let cod_pregunta_52 =  $('.formCaptacion input[data-cod-pregunta="52"]' );
    let cod_pregunta_53 =  $('.formCaptacion input[data-cod-pregunta="53"]' );
    let cod_pregunta_61 =  $('.formCaptacion input[data-cod-pregunta="61"]' );
    let cod_pregunta_71 =  $('.formCaptacion input[data-cod-pregunta="71"]' );
    let cod_pregunta_72 =  $('.formCaptacion input[data-cod-pregunta="72"]' );
    let cod_pregunta_73 =  $('.formCaptacion input[data-cod-pregunta="73"]' );
    let cod_pregunta_74 =  $('.formCaptacion input[data-cod-pregunta="74"]' );

    if (verificarExistencia(cod_pregunta_11)==false) {return false};
    if(validacionChecked(cod_pregunta_11)== false){return false};

    if (verificarExistencia(cod_pregunta_13)==false) {return false};
    if(validacionChecked(cod_pregunta_13)== false){return false};

    if (verificarExistencia(cod_pregunta_14)==false) {return false};
    if(validacionChecked(cod_pregunta_14)== false){return false};

    if (verificarExistencia(cod_pregunta_15)==false) {return false};
    if(validacionChecked(cod_pregunta_15)== false){return false};

    if (verificarExistencia(cod_pregunta_21) != false) {
        if(validacionChecked(cod_pregunta_21)== false){
            return false
        };
    };

    if (verificarExistencia(cod_pregunta_22) != false) {
        if(validacionChecked(cod_pregunta_22)== false){
            return false
        };
    };

    if (verificarExistencia(cod_pregunta_41) != false) {
        if(validacionChecked(cod_pregunta_41)== false){
            return false
        };
    };

    if (verificarExistencia(cod_pregunta_51) != false) {
        if(validacionChecked(cod_pregunta_51)== false){
            return false
        };
    };

    if (verificarExistencia(cod_pregunta_52) != false) {
        if(validacionChecked(cod_pregunta_52)== false){
            return false
        };
    };
    if (verificarExistencia(cod_pregunta_53) != false) {
        if(validacionChecked(cod_pregunta_53)== false){
            return false
        };
    };
    if (verificarExistencia(cod_pregunta_61) != false) {
        if(validacionChecked(cod_pregunta_61)== false){
            return false
        };
    };
    if (verificarExistencia(cod_pregunta_71) != false) {
        if(validacionChecked(cod_pregunta_71)== false){
            return false
        };
    };
    if (verificarExistencia(cod_pregunta_72) != false) {
        if(validacionChecked(cod_pregunta_72)== false){
            return false
        };
    };
    if (verificarExistencia(cod_pregunta_73) != false) {
        if(validacionChecked(cod_pregunta_73)== false){
            return false
        };
    };
    if (verificarExistencia(cod_pregunta_74) != false) {
        if(validacionChecked(cod_pregunta_74)== false){
            return false
        };
    };


}

const validate_component_entero = () => {

    let cod_pregunta_31 = $('.formCaptacion input[data-cod-pregunta="31"]');
    let cod_pregunta_32 = $('.formCaptacion input[data-cod-pregunta="32"]');
    let cod_pregunta_33 = $('.formCaptacion input[data-cod-pregunta="33"]');
    let cod_pregunta_34 = $('.formCaptacion input[data-cod-pregunta="34"]');
    let cod_pregunta_42 = $('.formCaptacion input[data-cod-pregunta="42"]');
    let cod_pregunta_62 = $('.formCaptacion input[data-cod-pregunta="62"]');
    let cod_pregunta_63 = $('.formCaptacion input[data-cod-pregunta="63"]');

    if (verificarExistencia(cod_pregunta_31) != false && verificarExistencia(cod_pregunta_32) != false && verificarExistencia(cod_pregunta_33) != false
        && verificarExistencia(cod_pregunta_34) != false && verificarExistencia(cod_pregunta_42) != false && verificarExistencia(cod_pregunta_62) != false
    && verificarExistencia(cod_pregunta_63) != false) {

        let suma_modelos = parseInt(cod_pregunta_32.val()) + parseInt(cod_pregunta_33.val()) + parseInt(cod_pregunta_34.val())

        if (cod_pregunta_31.val() < 0 || cod_pregunta_32.val() < 0 || cod_pregunta_33.val() < 0 || cod_pregunta_34.val() < 0 || cod_pregunta_42.val() < 0 || cod_pregunta_62.val() < 0 || cod_pregunta_63.val() < 0) {
            toastr.error("Verifique no haber entrado valores negativos.", 'Error', {
                progressBar: true,
                closeButton: true,
                "timeOut": "5000",
            });
            return false
        }

        if (cod_pregunta_31.val().length > 3 || cod_pregunta_32.val().length > 3 || cod_pregunta_33.val().length > 3 || cod_pregunta_34.val().length > 3) {
            toastr.error("Los campos vinculados a los reportes de modelos deben contener como maximo 3 digitos.", 'Error', {
                progressBar: true,
                closeButton: true,
                "timeOut": "5000",
            });
            return false
        }
        if (cod_pregunta_31.val() <= cod_pregunta_32.val()) {
            toastr.error("La cantidad de modelos " + cod_pregunta_32.prop('name') + " debe ser menor el que " + cod_pregunta_31.prop('name') + ".", 'Error', {
                progressBar: true,
                closeButton: true,
                "timeOut": "5000",
            });
            return false
        }
        if (cod_pregunta_31.val() <= cod_pregunta_33.val()) {
            toastr.error("La cantidad de modelos " + cod_pregunta_33.prop('name') + " debe ser menor el que " + cod_pregunta_31.prop('name') + ".", 'Error', {
                progressBar: true,
                closeButton: true,
                "timeOut": "5000",
            });
            return false
        }
        if (cod_pregunta_31.val() <= cod_pregunta_34.val()) {
            toastr.error("La cantidad de modelos " + cod_pregunta_34.prop('name') + " debe ser menor el que " + cod_pregunta_31.prop('name') + ".", 'Error', {
                progressBar: true,
                closeButton: true,
                "timeOut": "5000",
            });
            return false
        }
        if (parseInt(cod_pregunta_31.val()) !== suma_modelos) {
            toastr.error("El " + cod_pregunta_31.prop('name') + " no se corresponde con la suma entre: " + cod_pregunta_32.prop('name') + " " + cod_pregunta_33.prop('name') + " y " + cod_pregunta_34.prop('name') + ".", 'Error', {
                progressBar: true,
                closeButton: true,
                "timeOut": "5000",
            });
            return false
        }
    };


}

const validate_depedencias_campos = () => {

    let cod_pregunta_41_No =  $('.formCaptacion input[data-cod-pregunta="41"]:input[value="No"] ' );
    let cod_pregunta_41_Si =  $('.formCaptacion input[data-cod-pregunta="41"]:input[value="Si"] ' );
    let cod_pregunta_42 =  $('.formCaptacion input[data-cod-pregunta="42"]' );
    let cod_pregunta_61_No =  $('.formCaptacion input[data-cod-pregunta="61"]:input[value="No"] ' );
    let cod_pregunta_61_Si =  $('.formCaptacion input[data-cod-pregunta="61"]:input[value="Si"] ' );
    let cod_pregunta_62 =  $('.formCaptacion input[data-cod-pregunta="62"]' );
    let cod_pregunta_63 =  $('.formCaptacion input[data-cod-pregunta="63"]' );
    let cod_pregunta_71_No =  $('.formCaptacion input[data-cod-pregunta="71"]:input[value="No"] ' );
    let cod_pregunta_71_Si =  $('.formCaptacion input[data-cod-pregunta="71"]:input[value="Si"] ' );
    let cod_pregunta_711 =  $('.formCaptacion textarea[data-cod-pregunta="711"]' );
    let cod_pregunta_72_No =  $('.formCaptacion input[data-cod-pregunta="72"]:input[value="No"] ' );
    let cod_pregunta_72_Si =  $('.formCaptacion input[data-cod-pregunta="72"]:input[value="Si"] ' );
    let cod_pregunta_721 =  $('.formCaptacion textarea[data-cod-pregunta="721"]' );
    let cod_pregunta_73_No =  $('.formCaptacion input[data-cod-pregunta="73"]:input[value="No"] ' );
    let cod_pregunta_73_Si =  $('.formCaptacion input[data-cod-pregunta="73"]:input[value="Si"] ' );
    let cod_pregunta_731 =  $('.formCaptacion textarea[data-cod-pregunta="731"]' );
    let cod_pregunta_74_No =  $('.formCaptacion input[data-cod-pregunta="74"]:input[value="No"] ' );
    let cod_pregunta_74_Si =  $('.formCaptacion input[data-cod-pregunta="74"]:input[value="Si"] ' );
    let cod_pregunta_741 =  $('.formCaptacion textarea[data-cod-pregunta="741"]' );
    cod_pregunta_42.prop('readonly', true);
    cod_pregunta_62.prop('readonly', true);
    cod_pregunta_63.prop('readonly', true);
    cod_pregunta_711.prop('readonly', true).prop('value', "Ninguno");
    cod_pregunta_721.prop('readonly', true).prop('value', "");
    cod_pregunta_731.prop('readonly', true).prop('value', "");
    cod_pregunta_741.prop('readonly', true).prop('value', "");

    cod_pregunta_41_No.on('click', function () {
        cod_pregunta_42.prop('readonly', true);
    });
    cod_pregunta_41_Si.on('click', function () {
        cod_pregunta_42.prop('readonly', false);
    });
    cod_pregunta_61_No.on('click', function () {
        cod_pregunta_62.prop('readonly', true);
        cod_pregunta_63.prop('readonly', true);
    });
    cod_pregunta_61_Si.on('click', function () {
        cod_pregunta_62.prop('readonly', false);
        cod_pregunta_63.prop('readonly', false);
    });
    cod_pregunta_71_No.on('click', function () {
        cod_pregunta_711.prop('readonly', true).prop('value', "Ninguno");;
    });
    cod_pregunta_71_Si.on('click', function () {
        cod_pregunta_711.prop('readonly', false).prop('value', "");
    });
     cod_pregunta_72_No.on('click', function () {
        cod_pregunta_721.prop('readonly', false).prop('value', "");
    });
    cod_pregunta_72_Si.on('click', function () {
        cod_pregunta_721.prop('readonly', true).prop('value', "");
    });
     cod_pregunta_73_No.on('click', function () {
        cod_pregunta_731.prop('readonly', false).prop('value', "");
    });
    cod_pregunta_73_Si.on('click', function () {
        cod_pregunta_731.prop('readonly', true).prop('value', "");
    });
     cod_pregunta_74_No.on('click', function () {
        cod_pregunta_741.prop('readonly', false).prop('value', "");
    });
    cod_pregunta_74_Si.on('click', function () {
        cod_pregunta_741.prop('readonly', true).prop('value', "");
    })

}

validate_depedencias_campos();
//--------------------------------INICIALIZACION DE CAMPOS NUMERICOS EN SOBRE ENTIDAD--------------------------------------------//

let entero = $('.formCaptacion input[data-component="entero"]' );
for (var i=0; i<entero.length; i++){
    entero[i].value=0
}

//-----------------------------------------PROCEDIMIENTO PARA GUARDAR LO CAPTADO EN SOBRE ENTIDAD--------------------------------------------------//

let texto = $('.formCaptacion input[data-component="texto"]:text' );

$('form[class="formCaptacion"]').on('submit', function (e) {
    e.preventDefault();
    let  campos = new FormData(this);
    campos.forEach(function (value, key) {
        console.log(key+':'+value)
    })

    for (var i=0; i<texto.length; i++){
        if(texto[i].dataset.type ==="1" && texto[i].value === ""){
             toastr.error(texto[i].name+" es requerido.", 'Error', {
             progressBar: true,
             closeButton: true,
             "timeOut": "5000",
    });
             return false;
        }else{
            reg=/^[a-zA-Z]+$/;
            if(!reg.test(texto[i].value )){
                  toastr.error(texto[i].name+" debe contener solo letras.", 'Error', {
             progressBar: true,
             closeButton: true,
             "timeOut": "5000",
    });
                  return false;
            }
        }
    }
     if( validate_radios_no_empty() === false){return false};
     if( validate_component_entero() === false){return false};

    $.ajax({
        url: '/guia/dataCaptacion/',
        type: 'POST',
        data: campos,
        dataType: 'json',
        processData: false,
        contentType:false
    }).done(function (data) {
        if (data.hasOwnProperty('error')) {
            toastr.error(data.error, 'Error', {
                progressBar: true,
                closeButton: true,
                "timeOut": "5000",
            });
        } else {
            $('.desabilitar').removeClass("desabilitar");
            $('#cantCuestionario').load(' #cantCuestionario');
            toastr.success(data.exito, 'Exito', {
                progressBar: true,
                closeButton: true,
                "timeOut": "2000",
            });
        }
    }).fail(function (jqXHR, textStatus,errorThrown) {
        alert(textStatus+' : '+errorThrown)
    })
});


//-----------------------------------------PROCEDIMIENTO PARA GUARDAR LO CAPTADO EN EL FORM DE INSTANCIA--------------------------------------------------//

$('form[name="instanciaForm"]').on('submit', function (e) {
    e.preventDefault();
    let instancia_from_seccion = $(this).data('seccion');
    if(validate_no_empty_instancias(instancia_from_seccion, $('select[name="seccion_id"]')) === false){return false};
    if(validate_no_empty_instancias(instancia_from_seccion, $('select[name="columna_id"]')) === false){return false};
    if(validate_no_empty_instancias(instancia_from_seccion, $('select[name="codigo_id"]')) === false){return false};
    if(validate_no_empty_instancias(instancia_from_seccion, $('input[name="modelo_1"]')) === false){return false};
    if(validate_no_empty_instancias(instancia_from_seccion, $('input[name="registro_1"]')) === false){return false};
    if(validate_no_empty_instancias(instancia_from_seccion, $('input[name="modelo_2"]')) === false){return false};
    if(validate_no_empty_instancias(instancia_from_seccion, $('input[name="registro_2"]')) === false){return false};
    if(validate_no_empty_instancias(instancia_from_seccion, $('input[name="modelo_3"]')) === false){return false};
    if(validate_no_empty_instancias(instancia_from_seccion, $('input[name="registro_3"]')) === false){return false};
    let  campos = new FormData(this);
    $.ajax({
        url: '/guia/dataCaptacion/',
        type: 'POST',
        data: campos,
        dataType: 'json',
        processData: false,
        contentType: false
    }).done(function (data) {
       let modal = $('.instanciaModal');
        modal.modal('hide');
        $('button[name="actualizar"]').prop('disabled', false);
         tabla(actualizarTabla)
    }).fail(function (jqXHR, textStatus, errorThrown) {
        alert(textStatus + ' : ' + errorThrown)
    })
});


 //-------------------------------------------SELECT ENCADENADOS---------------------------------------------------------------

let select = $('select[name="seccion_id"]');
$('a[name="valor"]').on('click', function (e) {
        let id = $(this).data('id');
        let nombre = $(this).data('nombre');
        let options = '<option value="">--------</option>';
        options+='<option value="'+id+'">'+nombre+'</option>';
        select.html(options)
    });

 let selectCol = $('select[name="columna_id"]');
 $('select[name="seccion_id"]').on('change', function () {
     let id = $(this).val();
     $.ajax({
        url: '/seccion/getColumnas/',
        type: 'POST',
        data: {
            'action':'getColumnas',
            'id': id
        },
        dataType: 'json'
    }).done(function (data) {
        if(!data.hasOwnProperty('error')){
            selectCol.html('').select2({
                theme: "bootstrap4",
                language: 'es',
                data: data
            });
            return false
        }
    }).fail(function (jqXHR, textStatus,errorThrown) {
        alert(textStatus+' : '+errorThrown)
    });
 });

 let selectCod = $('select[name="codigo_id"]');
 $('select[name="columna_id"]').on('change', function () {
     let columna_id=$(this).val();
     let options = '<option value="">---------</option>';
     if (columna_id===''){
         selectCol.html(options)
     }
     $.ajax({
        url: '/seccion/getCodigos/',
        type: 'POST',
        data: {
            'action':'getCodigos',
            'id': columna_id
        },
        dataType: 'json'
    }).done(function (data) {
        if(!data.hasOwnProperty('error')){
            selectCod.html('').select2({
                theme: "bootstrap4",
                language: 'es',
                data: data
            });
            return false
        }
    }).fail(function (jqXHR, textStatus,errorThrown) {
        alert(textStatus+' : '+errorThrown)
    });
 });

 //----------------------------------------------PERSONALIZACION DE LA TABLA ENTIDAD------------------------------------------------------------------
$(document).ready(function () {

    let table = $('#entidadTable').DataTable({
        columnDefs: [{
            orderable: false,
            className: 'select-checkbox',
            targets: 0
        },{
           orderable: false,
            targets: 1
        },{
           orderable: false,
            targets: 2
        },{
           orderable: false,
            targets: 3
        },{
           orderable: false,
            targets: 4
        },{
           orderable: false,
            targets: 5
        },{
           orderable: false,
            targets: 6
        },{
           orderable: false,
            targets: 7
        },{
           orderable: false,
            targets: 8
        },{
           orderable: false,
            targets: 9
        },{
           orderable: false,
            targets: 10
        },{
           orderable: false,
            targets: 11
        },{
           orderable: false,
            targets: 12
        }],
        select: {
            style: 'multi',
            selector: 'td:first-child'
        },
        dom: 'Blfrtip',
        buttons: [
            'selectAll',
            'selectNone',
        ],
        language: {
            buttons: {
                selectAll: "Seleccionar todos",
                selectNone: "Deseleccionar todos"
            }
        },
    });

    // -----------------------------------------------CREACION DE FILTROS POR CADA COLUMNA-----------------------------------------

  $('#entidadTable thead tr').clone(true).appendTo('#entidadTable thead');

  $('#entidadTable thead tr:eq(1) th').each(function (i) {
      var title = $(this).text();
       $(this).html( '<input type="text" id="'+title+'1" placeholder="'+title+'" style="border-color: blue;border-top:0px;border-left:0px;border-right: 0px; width: 100%"/>' );

       $( 'input', this).on( 'keyup change ', function () {
                    if ( table.column(i ).search() !== this.value) {
                        table
                            .column(i)
                            .search(this.value)
                            .draw();
                    }
                });
  });
  $('#1').prop("hidden", true);
  $('#Acciones1').prop("hidden", true);

  //------------------------------------------------CREAR UNIVERSO DE LA GUIA--------------------------------------------------------------//

  $('#universo').on('click', function () {
    let selector = $('.selected');
    let array = [];
    for (var i=0; i < selector.length; i++){
        array.push(table.rows('.selected').data()[i][1]);
       }
    if(array.length === 0){
        toastr.error("Seleccione al menos una opcion para conformar el universo.", 'Error',{
        progressBar: true,
        closeButton: true,
        "timeOut": "3000",
    });
        return false
    }else {
    let valorJson = JSON.stringify(array);
        console.log(valorJson);
    $.ajax({
        url: '/guia/universo/',
        type: 'POST',
        data: {
            'action':'universo',
            'data': valorJson
        },
        dataType: 'json'
    }).done(function (data) {
        toastr.success(data.exito, 'Exito',{
        progressBar: true,
        closeButton: true,
        "timeOut": "3000",
    });
    }).fail(function (jqXHR, textStatus,errorThrown) {
        toastr.error(textStatus+' : '+errorThrown, 'Error',{
        progressBar: true,
        closeButton: true,
        "timeOut": "3000",
    })
    });
    }
});
});


$('div[data-model-name="modal"]').on('shown.bs.modal', function () {
    $('form[name="instanciaForm"]')[0].reset();
});

//-----------------------------------------------------------PARTE PARA MOSTRAR LO CAPTADO---------------------------------------
             //------------------------PREGUNTAS EVALUADAS Y SECCIONES----------------------//

$('#detalles_preguntasEvaluadas').prop("hidden", true);
$('#modificacionPreguntas').prop("hidden", true);
$('#modificarInstancias').prop("hidden", true);

$('.ocultar').on('click', function () {
    $('#detalles_preguntasEvaluadas').prop("hidden", true);
    $('#modificacionPreguntas').prop("hidden", true);
    $('#modificarInstancias').prop("hidden", true);
});

$('a[name="detalles"]').on('click', function () {
    var id = $(this).data('id');
    $.ajax({
        url: '/guia/informacionCaptada/',
        type: 'POST',
        data: {
            'action': 'informacionCaptada',
            'id': id
        },
        dataType: 'json'
    }).done(function (data) {
        $('#detalles_preguntasEvaluadas').prop("hidden", false);
        var contenido = $('#contenido');
        var informacion = '<h1></h1>';
        for (var i = 0; i < data.length; i++) {
            if (data[i].pregunta != null){
             informacion += '<h6 class="text-bold text-uppercase">'+ '<span class="badge bg-gradient-primary" style="width: 100%; padding: 10px">'+ data[i].pregunta + '</span>'+'</h6>'+'<h6 class="text-bold text-center text-uppercase" >'+ data[i].respuesta + '</h6>' +'<hr>'

            }
        }
         var table = '<table class="table table-bordered table-striped" >' +
             '<thead class="bg-gradient-primary text-bold"><tr><td>Seccion</td>' +
             '<td>Codigo</td>' +
             '<td>No.Col</td>' +
             '<td>Modelo</td>' +
             '<td>Registro</td>' +
             '<td>Dif.</td>' +
             '<td>Modelo</td>' +
             '<td>Registro</td>' +
             '<td>Dif.</td>' +
             '<td>Modelo</td>' +
             '<td>Registro</td>' +
             '<td>Dif.</td>' +
             '</tr></thead><tbody>';
             for (var i = 0; i < data.length; i++) {
                 if (data[i].seccion_id != null) {
                     table += '<tr><td>' + '<span class="badge bg-gradient-navy" style="padding: 3px">'+ data[i].seccion_id + '</span>' + '</td>' +
                         '<td>' + data[i].codigo_id + '</td>' +
                         '<td>' + data[i].columna_id + '</td>' +
                         '<td>' + data[i].modelo_1 + '</td>' +
                         '<td>' + data[i].registro_1 + '</td>' +
                         '<td>' + '<span class="badge bg-danger" style="padding: 3px">'+ data[i].diferencia_1 + '</span>' + '</td>' +
                         '<td>' + data[i].modelo_2 + '</td>' +
                         '<td>' + data[i].registro_2 + '</td>' +
                         '<td>' + '<span class="badge bg-danger" style="padding: 3px">'+ data[i].diferencia_2 + '</span>'+ '</td>' +
                         '<td>' + data[i].modelo_3 + '</td>' +
                         '<td>' + data[i].registro_3 + '</td>' +
                         '<td>' + '<span class="badge bg-danger" style="padding: 3px">'+ data[i].diferencia_3 + '</span></td></tr>'
                 }
             }
             table += '</tbody></table>'
         contenido.html(informacion + table);
    }).fail(function (jqXHR, textStatus, errorThrown) {
        alert(textStatus + ' : ' + errorThrown)
    });
});

//-----------------------------------CONTROL DE ACCESOS-------------------------------------------//

$('#widgetGuia').on('click', function () {
     $('#widgetGuia').prop("disabled", true);
         toastr.error('Lo sentimos no tiene los permisos requeridos para realizar esta accion.', 'Acceso denegado',{
        progressBar: true,
        closeButton: true,
        "timeOut": "3000",
    })
});

$('#widgetEntidad').on('click', function () {
     $('#widgetEntidad').prop("disabled", true);
         toastr.error('Lo sentimos no tiene los permisos requeridos para realizar esta accion.', 'Acceso denegado',{
        progressBar: true,
        closeButton: true,
        "timeOut": "3000",
    })
});

$('#widgetUsuario').on('click', function () {
     $('#widgetUsuario').prop("disabled", true);
         toastr.error('Lo sentimos no tiene los permisos requeridos para realizar esta accion.', 'Acceso denegado',{
        progressBar: true,
        closeButton: true,
        "timeOut": "3000",
    })
});

//--------------------------------MODIFICACIONES DE LAS COSAS CAPTADAS DEL CUESTIONARIO---------------------------------------------//

//-----------1. PREGUNTAS---------------//

$('a[name="modificarPreguntas"]').on('click', function () {
    var id = $(this).data('id');
    var form = $('#contenidoEdicionPreguntas');
    var campos = '<input type="hidden" name="action" value="modificarPreguntas"><input type="hidden" name="id" value="'+id+'">';
    $.ajax({
        url: '/guia/modificarPreguntas/',
        type: 'POST',
        data: {
            'action': 'cargarPreguntas',
            'id': id
        },
        dataType: 'json',
    }).done(function (data) {
        $('#modificacionPreguntas').prop("hidden", false);
        for (var i = 0; i < data.length; i++) {
           if (data[i].pregunta === "Entidad"){
               campos += '<div class="form-group"><label>'+data[i].pregunta+'</label><input class="form-control" type="text" name="'+data[i].pregunta+'" readonly value="'+data[i].respuesta+'"></div>'
           }else {
               campos += '<div class="form-group"><label>'+data[i].pregunta+'</label><input class="form-control" type="text" name="'+data[i].pregunta+'" value="'+data[i].respuesta+'"></div>'
           }
       }
        campos+='<div class="form-actions"><div class="row"><div class="offset-md-10 col-2"><button type=submit class="btn btn-primary"><i class="fa fa-save "></i> Salvar</button></div></div></div>'
        form.html(campos)
    }).fail(function (jqXHR, textStatus,errorThrown) {
        alert(textStatus+' : '+errorThrown)
    })
});

$('form[name="contenidoEdicionPreguntas"]').on('submit', function (e) {
    e.preventDefault();
    var  campos = new FormData(this);
    $.ajax({
        url: '/guia/modificarPreguntas/',
        type: 'POST',
        data: campos,
        dataType: 'json',
        processData: false,
        contentType:false
    }).done(function (data) {
        $('#modificacionPreguntas').prop("hidden", true);
        toastr.success("Las preguntas del cuestionario han sido modificadas correctamente.", 'Exito',{
        progressBar: true,
        closeButton: true,
        "timeOut": "3000",
    });
    }).fail(function (jqXHR, textStatus,errorThrown) {
        alert(textStatus+' : '+errorThrown)
    })
});

//-----------1. INSTANCIAS---------------//

$('a[name="modificarInstancias"]').on('click', function () {
    var id = $(this).data('id');
    var form = $('#contenidoEdicionInstancias');
    var campos = '<input type="hidden" name="action" value="modificarInstancias">' +
        '<table class="table table-bordered table-striped" >' +
        '<thead class="bg-gradient-primary text-bold"><tr><td>No.Instancia</td>' +
        '<td>Seccion</td>' +
        '<td>Codigo</td>' +
        '<td>No.Col</td>' +
        '<td>Modelo</td>' +
        '<td>Registro</td>' +
        '<td>Modelo</td>' +
        '<td>Registro</td>' +
        '<td>Modelo</td>' +
        '<td>Registro</td>' +
        '</tr></thead><tbody>';
    $.ajax({
        url: '/seccion/modificarInstancias/',
        type: 'POST',
        data: {
            'action': 'cargarInstancias',
            'id': id
        },
        dataType: 'json',
    }).done(function (data) {
        console.log(data);
        $('#modificarInstancias').prop("hidden", false);
        for (var i = 0; i < data.length; i++) {
           campos+= '<tr><td><input type="number" class="form-control" name="id" readonly value="'+ data[i].id +'"></td>' +
                    '<td><input type="text" class="form-control" name="seccion" readonly value="'+ data[i].seccion_id +'"></td>' +
                    '<td><input type="number" class="form-control" name="codigo" readonly value="'+ data[i].codigo_id +'"></td>' +
                    '<td><input type="number" class="form-control" name="columna" readonly value="'+ data[i].columna_id +'"></td>' +
                    '<td><input type="number" class="form-control" name="modelo_1" value="'+ data[i].modelo_1 +'"></td>' +
                    '<td><input type="number" class="form-control" name="registro_1" value="'+ data[i].registro_1 +'"></td>' +
                    '<td><input type="number" class="form-control" name="modelo_2" value="'+ data[i].modelo_2 +'"></td>' +
                    '<td><input type="number" class="form-control" name="registro_2" value="'+ data[i].registro_2 +'"></td>' +
                    '<td><input type="number" class="form-control" name="modelo_3" value="'+ data[i].modelo_3 +'"></td>' +
                    '<td><input type="number" class="form-control" name="registro_3" value="'+ data[i].registro_3 +'"></td></tr>'
       }
        campos+='</tbody></table><div class="form-actions"><div class="row"><div class="offset-md-10 col-2"><button type=submit class="btn btn-primary"><i class="fa fa-save "></i> Salvar</button></div></div></div>'
        form.html(campos)
    }).fail(function (jqXHR, textStatus,errorThrown) {
        alert(textStatus+' : '+errorThrown)
    })
});


$('form[name="contenidoEdicionInstancias"]').on('submit', function (e) {
    e.preventDefault();
    var  campos = new FormData(this);
    $.ajax({
        url: '/seccion/modificarInstancias/',
        type: 'POST',
        data: campos,
        dataType: 'json',
        processData: false,
        contentType:false
    }).done(function (data) {
        alert(data);
        $('#modificarInstancias').prop("hidden", true);
        toastr.success("Las instancias del cuestionario han sido modificadas correctamente.", 'Exito',{
        progressBar: true,
        closeButton: true,
        "timeOut": "3000",
    });
    }).fail(function (jqXHR, textStatus,errorThrown) {
        alert(textStatus+' : '+errorThrown)
    })
});

$('.acordeon').on('click', function () {
    console.log($('.registro'))
    $('.formVerificacion').prop('hidden', true)
    var seccionAcordion=$(this).data('seccion')
    console.log(seccionAcordion)
    for (var i=0;i,i<$('.registro').length; i++){
        if (seccionAcordion === $('.registro')[i].dataset.seccionRegistro && $('.registro')[i].textContent !== "") {
            $('.formVerificacion').prop('hidden', false)
        }
    }
});


//-------------------------------VALIDACIONS DENTRO DE LOS FORMULARIOS DENTRO DE LA SECCION ADMIN--------------------------//

$(' #guiaForm').bootstrapValidator({
    message: 'This value is not valid',
    feedbackIcons: {
        valid: 'glyphicon glyphicon-ok',
        invalid: 'fa fa-times-circle',
        validating: 'glyphicon glyphicon-refresh'
    },
    fields: {
        nombre: {
            message: 'El nombre no es valido',
            validators: {
                notEmpty: {
                    message: 'El nombre es requerido'
                },
                regexp: {
                    regexp: /^[a-zA-ZñÑáéíóú_ ]+$/,
                    message: 'El nombre debe contener solo letras'
                }

            }
        },
    }
});

$(' #entidadForm').bootstrapValidator({
    message: 'This value is not valid',
    feedbackIcons: {
        valid: 'glyphicon glyphicon-ok',
        invalid: 'fa fa-times-circle',
        validating: 'glyphicon glyphicon-refresh'
    },
    fields: {
        codigo_CI: {
            message: 'El codigo no es valido',
            validators: {
                notEmpty: {
                    message: 'El codigo es requerido.'
                },
                stringLength: {
                        min: 6,
                        max: 6,
                        message: 'El codigo debe ser de 6 digitos'
                    },
                regexp: {
                    regexp: /^[0-9]+$/,
                    message: 'Solo se admiten digitos.'
                }

            }
        },
        nombre_CI: {
            message: 'El nombre no es valido',
            validators: {
                notEmpty: {
                    message: 'El nombre es requerido'
                },

            }
        },
        ote_codigo: {
            message: 'El nombre no es valido',
            validators: {
                notEmpty: {
                    message: 'Campo requerido. Debe seleccionar una opcion'
                },

            }
        },
        ome_codigo: {
            message: 'El nombre no es valido',
            validators: {
                notEmpty: {
                    message: 'Campo requerido. Debe seleccionar una opcion'
                },

            }
        },
        codigo_NAE: {
            message: 'El nombre no es valido',
            validators: {
                notEmpty: {
                    message: 'Campo requerido. Debe seleccionar una opcion'
                },

            }
        },
        org_codigo: {
            message: 'El nombre no es valido',
            validators: {
                notEmpty: {
                    message: 'Campo requerido. Debe seleccionar una opcion'
                },

            }
        },
        osde_codigo: {
            message: 'El nombre no es valido',
            validators: {
                notEmpty: {
                    message: 'Campo requerido. Debe seleccionar una opcion'
                },

            }
        },


    }
});

$(' #periodoForm').bootstrapValidator({
    message: 'This value is not valid',
    feedbackIcons: {
        valid: 'glyphicon glyphicon-ok',
        invalid: 'fa fa-times-circle',
        validating: 'glyphicon glyphicon-refresh'
    },
    fields: {
        tipo: {
            message: 'El nombre no es valido',
            validators: {
                notEmpty: {
                    message: 'El tipo de periodo es requerido'
                },

            }
        },
        mes_1: {
            message: 'El nombre no es valido',
            validators: {
                notEmpty: {
                    message: 'Campo requerido. Debe seleccionar una opcion'
                },

            }
        },
        ano_1: {
            message: 'El nombre no es valido',
            validators: {
                notEmpty: {
                    message: 'Campo requerido. Debe seleccionar una opcion'
                },

            }
        },


    }
});

$(' #seccionForm').bootstrapValidator({
    message: 'This value is not valid',
    feedbackIcons: {
        valid: 'glyphicon glyphicon-ok',
        invalid: 'fa fa-times-circle',
        validating: 'glyphicon glyphicon-refresh'
    },
    fields: {
        nombre: {
            message: 'El nombre no es valido',
            validators: {
                notEmpty: {
                    message: 'El nombre es requerido'
                },
                regexp: {
                    regexp: /^[a-zA-ZñÑáéíóú_]+$/,
                    message: 'El campo nombre no debe tener especios en blanco.'
                }

            }
        },
        guia_id: {
            message: 'El nombre no es valido',
            validators: {
                notEmpty: {
                    message: 'Campo requerido. Debe seleccionar una opcion'
                },

            }
        },
        orden: {
            message: 'El nombre no es valido',
            validators: {
                notEmpty: {
                    message: 'El orden es requerido'
                },
            }
        },


    }
});

$(' #codigoForm').bootstrapValidator({
    message: 'This value is not valid',
    feedbackIcons: {
        valid: 'glyphicon glyphicon-ok',
        invalid: 'fa fa-times-circle',
        validating: 'glyphicon glyphicon-refresh'
    },
    fields: {
        codigo: {
            message: 'El nombre no es valido',
            validators: {
                notEmpty: {
                    message: 'El codigo es requerido'
                },
                regexp: {
                    regexp: /^[0-9]+$/,
                    message: 'Solo se admiten digitos.'
                }

            }
        },
        descripcion: {
            message: 'El nombre no es valido',
            validators: {
                notEmpty: {
                    message: 'El campo descripcion es requerido'
                },

            }
        },

    }
});

$(' #columnaForm').bootstrapValidator({
    message: 'This value is not valid',
    feedbackIcons: {
        valid: 'glyphicon glyphicon-ok',
        invalid: 'fa fa-times-circle',
        validating: 'glyphicon glyphicon-refresh'
    },
    fields: {
        seccion_id: {
            message: 'El nombre no es valido',
            validators: {
                notEmpty: {
                    message: 'Campo requerido. Debe seleccionar una opcion'
                },

            }
        },
        codigo_id: {
            message: 'El nombre no es valido',
            validators: {
                notEmpty: {
                    message: 'Campo requerido. Seleccione al menos una opcion.'
                },

            }
        },
        columna: {
            message: 'El nombre no es valido',
            validators: {
                notEmpty: {
                    message: 'La columna es requerida.'
                },
                regexp: {
                    regexp: /^[0-9]+$/,
                    message: 'Solo se admiten digitos.'
                }

            }
        },
        descripcion: {
            message: 'El nombre no es valido',
            validators: {
                notEmpty: {
                    message: 'El campo descripcion es requerido'
                },

            }
        },

    }
});

$(' #clasificadorIndForm').bootstrapValidator({
    message: 'This value is not valid',
    feedbackIcons: {
        valid: 'glyphicon glyphicon-ok',
        invalid: 'fa fa-times-circle',
        validating: 'glyphicon glyphicon-refresh'
    },
    fields: {
        seccion_id: {
            message: 'El nombre no es valido',
            validators: {
                notEmpty: {
                    message: 'Campo requerido. Debe seleccionar una opcion'
                },

            }
        },
        nombre: {
            message: 'El nombre no es valido',
            validators: {
                notEmpty: {
                    message: 'El nombre es requerido'
                },
                regexp: {
                    regexp: /^[a-zA-ZñÑáéíóú_ ]+$/,
                    message: 'Solo se admiten letras'
                }

            }
        },

    }
});

$(' #indicadoresForm').bootstrapValidator({
    message: 'This value is not valid',
    feedbackIcons: {
        valid: 'glyphicon glyphicon-ok',
        invalid: 'fa fa-times-circle',
        validating: 'glyphicon glyphicon-refresh'
    },
    fields: {
        clasificadorIndicadores_id: {
            message: 'El nombre no es valido',
            validators: {
                notEmpty: {
                    message: 'Campo requerido. Debe seleccionar una opcion'
                },

            }
        },
        respuestas_id: {
            message: 'El nombre no es valido',
            validators: {
                notEmpty: {
                    message: 'Campo requerido. Debe seleccionar al menos una opcion'
                },

            }
        },
        nombre: {
            message: 'El nombre no es valido',
            validators: {
                notEmpty: {
                    message: 'El campo nombre es requerido'
                },
                regexp: {
                    regexp: /^[a-zA-ZñÑáéíóú_ ]+$/,
                    message: 'Solo se admiten letras'
                }

            }
        },

    }
});

$(' #respuestasForm').bootstrapValidator({
    message: 'This value is not valid',
    feedbackIcons: {
        valid: 'glyphicon glyphicon-ok',
        invalid: 'fa fa-times-circle',
        validating: 'glyphicon glyphicon-refresh'
    },
    fields: {
        tipo_dato: {
            message: 'El nombre no es valido',
            validators: {
                notEmpty: {
                    message: 'Campo requerido. Debe seleccionar una opcion'
                },

            }
        },
        nombre: {
            message: 'El nombre no es valido',
            validators: {
                notEmpty: {
                    message: 'El campo nombre es requerido'
                },
                regexp: {
                    regexp: /^[a-zA-ZñÑáéíóú_ ]+$/,
                    message: 'Solo se admiten letras'
                }

            }
        },

    }
});

$('#userForm').bootstrapValidator({
        message: 'This value is not valid',
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
        invalid: 'fa fa-times-circle',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            first_name: {
                message: 'El nombre no es valido',
                validators: {
                    notEmpty: {
                        message: 'El nombre es requerido'
                    },

                regexp: {
                    regexp: /^[a-zA-ZñÑáéíóú_ ]+$/,
                    message: 'El nombre debe contener solo letras'
                }
                }
            },
            last_name: {
                message: 'El apellido no es valido',
                validators: {
                    notEmpty: {
                        message: 'El apellido es requeridoo'
                    },
                    regexp: {
                    regexp: /^[a-zA-ZñÑáéíóú_ ]+$/,
                    message: 'Los apellidos debe contener solo letras'
                }
                }
            },
            username: {
                message: 'El usuario no es valido',
                validators: {
                    notEmpty: {
                        message: 'El usuario es obligatorio'
                    },
                    stringLength: {
                        min: 3,
                        max: 30,
                        message: 'El usuario debe tener un minimo de 3 caracteres y un maximo de 30'
                    },
                    regexp: {
                        regexp: /^[a-zA-Z0-9]+$/,
                        message: 'EL usuario solo debe contener letras y numeros'
                    },
                    different: {
                        field: 'password1',
                        message: 'El usuario debe ser diferente a la contraseña'
                    }
                }
            },
            password: {
                validators: {
                    notEmpty: {
                        message: 'El campo contraseña es requerido.'
                    },
                    different: {
                        field: 'username',
                        message: 'La contraseña debe ser diferente del usuario'
                    },
                    stringLength: {
                        min: 8,
                        message: 'La contraseña debe tener como minimo 8 caracteres'
                    },
                    callback: {
                        callback: function(value, validator) {
                            if (value === value.toLowerCase()) {
                                return {
                                    valid: false,
                                    message: ' La contraseña debe contener mayusculas'
                                }
                            }
                            if (value === value.toUpperCase()) {
                                return {
                                    valid: false,
                                    message: 'La contraseña debe contener minusculas'
                                }
                            }
                             if (value.search(/[.*,@_]/) < 0) {
                                return {
                                    valid: false,
                                    message: 'La contraseña debe contener caracteres especiales (.*,@_)'
                                }
                            }
                            return true;
                        }
                    }
                }
            },
        }
    });

//------------------PORCEDIMIENTO PARA CREAR UNA GUIA CON LAS MISMAS CONFIGURACIONES DE OTRA YA DEFINIDA-----------------------//
 const url = () => {
           location.href='http://127.0.0.1:8000/guia/listarGuias/';
       }
guias = $('#listadoGuiasDefinidas');
buttonSafe = $('#safe');
checkboxGuias = $('#guiasDefinidas');
salvadoNormal = $('#salvadoNormal');

checkboxGuias.on('click', function () {
    if(checkboxGuias.is(':checked')==true){
   guias.prop('disabled', false);
   buttonSafe.prop('disabled', false);
   salvadoNormal.prop('disabled', true)

}else {
     guias.prop('disabled', true);
   buttonSafe.prop('disabled', true);
        salvadoNormal.prop('disabled', false)
}
});

$('#safe').on('click', function () {
    guiaNombre = $('#guiaNombre');
    guiaActiva = $('#guiaActiva');
    if(guias.val()===guiaNombre.val()){
        toastr.error("El nombre de la guia a crear ya existe.", 'Error',{
        progressBar: true,
        closeButton: true,
        "timeOut": "3000",
    });
        return false
    }
    $.ajax({
        url: '/guia/crearGuiaDefinida/',
        type: 'POST',
        data: {
            'action':'creacionDeGuia',
            'guiaNueva': guiaNombre.val(),
            'guiaYaDefinida': guias.val(),
            'activo':guiaActiva[0].checked
        },
        dataType: 'json',
    }).done(function (data) {
        toastr.success(data.exito, 'Exito', {
                progressBar: true,
                closeButton: true,
                "timeOut": "1500",
            });
        setTimeout (url,1500);
    }).fail(function (jqXHR, textStatus,errorThrown) {
        alert(textStatus+' : '+errorThrown)
    })

})

//---------------------------------PORCEDIMIENTO PARA El REPORTE DE VERIFICACION--------------------------------------//
 $('#reporteVerificacion').DataTable({
     dom: "Bfrtip",
     buttons: {
         dom: {
             button: {
                 className: 'btn fas fa-file-alt'
             }
         },
         buttons: [
             {
                 extend: "excel",
                 text: ' Exportar excel',
                 title: 'Reporte de Verificacion',
                 className: "btn btn-outline-primary",
                 excelStyles: {
                     template: "blue_medium",
                 },
             },
         ]
     }
 });

//--------------------------------------PORCEDIMIENTO PARA El REPORTE GENERAL---------------------------------------------//
 $('#reporteGeneral').DataTable({
     scrollX:true,
     dom: "Bfrtip",
     buttons: {
         dom: {
             button: {
                 className: 'btn fas fa-file-alt'
             }
         },
         buttons: [
             {
                 extend: "excel",
                 text: ' Exportar excel',
                 title: 'Reporte General',
                 className: "btn btn-outline-primary",
                 excelStyles: {
                     template: "blue_medium",
                 },
             },
         ]
     }
 });

 //--------------------------PORCEDIMIENTO PARA El REPORTE DE DISCIPLINA INFORMATIVA----------------------------------//
 $('#reporteDisciplinaInfo').DataTable({
     dom: "Bfrtip",
     buttons: {
         dom: {
             button: {
                 className: 'btn fas fa-file-alt'
             }
         },
         buttons: [
             {
                 extend: "excel",
                 text: ' Exportar excel',
                 title: 'Reporte de Disciplina Informativa',
                 className: "btn btn-outline-primary",
                 excelStyles: {
                     template: "blue_medium",
                 },
             },
         ]
     }
 });

 //---------------------------------PORCEDIMIENTO PARA El REPORTE DE SEÑALAMIENTO DE ERRORES-----------------------------//
 $('#reporteErrores').DataTable({
     dom: "Bfrtip",
     buttons: {
         dom: {
             button: {
                 className: 'btn fas fa-file-alt'
             }
         },
         buttons: [
             {
                 extend: "excel",
                 text: ' Exportar excel',
                 title: 'Reporte de Señalamientos de Errores',
                 className: "btn btn-outline-primary",
                 excelStyles: {
                     template: "blue_medium",
                 },
             },
         ]
     }
 });

 //---------------------------PORCEDIMIENTO PARA El REPORTE DE Displina info Centro Controlado-----------------------------//
 $('#reporteDisciplinaInfoCentroControlados').DataTable({
     dom: "Bfrtip",
     buttons: {
         dom: {
             button: {
                 className: 'btn fas fa-file-alt'
             }
         },
         buttons: [
             {
                 extend: "excel",
                 text: ' Exportar excel',
                 title: 'Reporte de Disciplina Informativa Centros Controlados',
                 className: "btn btn-outline-primary",
                 excelStyles: {
                     template: "blue_medium",
                 },
             },
         ]
     }
 });

 //------------------------------PORCEDIMIENTO PARA El REPORTE DE Domicilio Social Incorrecto-----------------------------//
 $('#reporteDomicilioSocial').DataTable({
     dom: "Bfrtip",
     buttons: {
         dom: {
             button: {
                 className: 'btn fas fa-file-alt'
             }
         },
         buttons: [
             {
                 extend: "excel",
                 text: ' Exportar excel',
                 title: 'Reporte de Domicilio Social Incorrecto',
                 className: "btn btn-outline-primary",
                 excelStyles: {
                     template: "blue_medium",
                 },
             },
         ]
     }
 });

 //---------------------------------PORCEDIMIENTO PARA El REPORTE DE Deficiencias-----------------------------//
 $('#reporteDeficiencias').DataTable({
     dom: "Bfrtip",
     buttons: {
         dom: {
             button: {
                 className: 'btn fas fa-file-alt'
             }
         },
         buttons: [
             {
                 extend: "excel",
                 text: ' Exportar excel',
                 title: 'Reporte de Deficiencias',
                 className: "btn btn-outline-primary",
                 excelStyles: {
                     template: "blue_medium",
                 },
             },
         ]
     }
 });

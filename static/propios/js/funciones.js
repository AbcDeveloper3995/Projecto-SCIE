//--------------------------------------------------------INICIALIZACIONES----------------------------------------------------------//
$('#dataTable').dataTable({});
let tblEntidad = $('#entidadTable').DataTable({
        select: true,
        select: {
            style: 'multi',
        },
        deferRender: true,
        ajax: {
            url: '/entidad/listarEntidad/',
            type: 'POST',
            data: {
                'action': 'getEntidades',
            },
            dataSrc: ""
        },
        columns: [
            {"data": "codigo_CI"},
            {"data": "nombre_CI"},
            {"data": "ote_codigo"},
            {"data": "ote_descripcion"},
            {"data": "ome_codigo"},
            {"data": "ome_descripcion"},
            {"data": "codigo_NAE"},
            {"data": "codigo_NAE_descripcion"},
            {"data": "osde_codigo"},
            {"data": "osde_descripcion"},
            {"data": "org_codigo"},
            {"data": "org_descripcion"},
            {"data": "id"},
        ],
        columnDefs: [{
            orderable: false,
            targets: 0
        }, {
            orderable: false,
            targets: 1
        }, {
            orderable: false,
            targets: 2
        }, {
            orderable: false,
            targets: 3
        }, {
            orderable: false,
            targets: 4
        }, {
            orderable: false,
            targets: 5
        }, {
            orderable: false,
            targets: 6
        }, {
            orderable: false,
            targets: 7
        }, {
            orderable: false,
            targets: 8
        }, {
            orderable: false,
            targets: 9
        }, {
            orderable: false,
            targets: 10
        }, {
            orderable: false,
            targets: 11
        }, {
            orderable: false,
            targets: 12
        }, {
            targets: [-1],
            class: 'text-center',
            orderable: false,
            render: function (data, type, row) {
                let buttons = '<a href="/entidad/modificarEntidad/' + row.id + '/"   type="button" ><i  class="fa fa-edit"></i></a>';
                buttons += '<a href="#"  rel="eliminarEntidad" type="button"><i class="fa fa-trash"></i></a>';
                return buttons;
            }
        }],
    });

$('.select2').select2({
    theme: 'bootstrap4',
    language: 'es',
    placeholder: 'Seleccione una opcion'
});

new WOW().init();


new tippy('.miTippy', {
    animation: 'perspective',
});

//---------------------------PROCEDIMIENTO PARA ACTUALIZAR EN TIEMPO REAL LOS DATOS EN LAS TABLAS--------------------//

const tabla = (nombreSeccion, idSeccion, idCuestionario) => {
    let nombre_seccion = "table" + nombreSeccion;
    let form_verificacion = $('.formVerificacion');
    let datatable = $('.' + nombre_seccion).DataTable({
        deferRender: true,
        destroy: true,
        ajax: {
            url: '/guia/captarDatos/',
            type: 'POST',
            data: {
                'action': 'mostrarInstancias',
                'id_seccion': idSeccion,
                'id_cuestionario': idCuestionario,
            },
            dataSrc: ""
        },
        columns: [
            {"data": "codigo_id"},
            {"data": "columna_id"},
            {"data": "registro_1"},
            {"data": "modelo_1"},
            {"data": "diferencia_1"},
            {"data": "registro_2"},
            {"data": "modelo_2"},
            {"data": "diferencia_2"},
            {"data": "registro_3"},
            {"data": "modelo_3"},
            {"data": "diferencia_3"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {

                    let buttons = '<a href="#"  rel="edit" type="button" ><i  class="fa fa-edit"></i></a>';
                    buttons += '<a href="/seccion/eliminarInstancia/' + row.id + '/" rel="remove" type="button"><i class="fa fa-trash"></i></a>';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {
            if (json.codigo_id !== "0") {
                for (var i = 0; i < form_verificacion.length; i++) {
                    if (idSeccion === parseInt(form_verificacion[i].dataset.id)) {
                        form_verificacion.prop('hidden', false);
                        // AJAX PARA OBTENER LA CANTIDAD DE INDICADORES VERIFICADOS DE CADA SECCION EVALUADA
                        $.ajax({
                            url: '/seccion/valorIndVerificado/',
                            type: 'POST',
                            data: {
                                'action': 'getValorIndVerificados',
                                'idSeccion': idSeccion,
                                'idCuestionario': idCuestionario,
                            },
                            dataType: 'json',
                        }).done(function (data) {
                            $('input[name=indicadoresVerificados]:input[data-seccion=' + nombreSeccion + ']').prop('value', data.cantidad)
                        }).fail(function (jqXHR, textStatus, errorThrown) {
                            alert(textStatus + ' : ' + errorThrown)
                        });
                        // AJAX PARA OBTENER LA CANTIDAD DE INDICADORES qQUE COINCIDEN DE CADA SECCION EVALUADA
                        $.ajax({
                            url: '/seccion/indicadoresCoinciden/',
                            type: 'POST',
                            data: {
                                'action': 'indicadoresCoinciden',
                                'idSeccion': idSeccion,
                                'idCuestionario': idCuestionario,
                            },
                            dataType: 'json',
                        }).done(function (data) {
                            $('input[name=indicadoresCoinciden]:input[data-seccion=' + nombreSeccion + ']').prop('value', data.cantidad)
                        }).fail(function (jqXHR, textStatus, errorThrown) {
                            alert(textStatus + ' : ' + errorThrown)
                        });
                        return false;
                    }
                }
            }
        }
    });
    let modalTitle = $('.title-editar');
    $('.' + nombre_seccion + ' tbody').on('click', 'a[rel="remove"]', function () {
        let tr = datatable.cell($(this).closest('td, li')).index();
        datatable.row(':eq(' + tr.row + ')').remove().draw()
    }).on('click', 'a[rel="edit"]', function () {
        let tr = datatable.cell($(this).closest('td, li')).index();
        let data = datatable.row(':eq(' + tr.row + ')').data();
        modalTitle.html('<i  class="fa fa-edit"></i> Edición de un instancia de la sección ' + data.seccion_id + ' <span class="badge badge-danger"> ' + data.numero + '</span>');
        $('label[id="labelModelo1"]').html('' + data.numero + '');
        $('label[id="labelModelo2"]').html('' + data.numero + '');
        $('label[id="labelModelo3"]').html('' + data.numero + '');
        $('input[name="idInstancia"]').val(data.id);
        $('input[name="1_registro"]').val(data.registro_1);
        $('input[name="1_modelo"]').val(data.modelo_1);
        $('input[name="2_registro"]').val(data.registro_2);
        $('input[name="2_modelo"]').val(data.modelo_2);
        $('input[name="3_registro"]').val(data.registro_3);
        $('input[name="3_modelo"]').val(data.modelo_3);
        $('#modalEditarInstancia' + data.seccion_id + '').modal('show');
    });
    console.log(datatable)



};


//---------------------------------------------VALIDACIONES DE FECHAS------------------------------------------------//

$('.date').datetimepicker({
    format: 'DD/MM/YYYY',
    date: moment().format("YYYY-MM-DD"),
    locale: 'es',
    maxDate: moment().format("YYYY-MM-DD"),
});



//--------------------------------------VALIDACIONES PARA EL FORM INSTANCIAS---------------------------------------------//

const validateInstancias = (seccionForm, seccionCampo) => {
    for (var i = 0; i < seccionCampo.length; i++) {
        // Validar que no hayan campos vacios//
        if (seccionForm === seccionCampo[i].dataset.seccion && seccionCampo[i].value === "") {
            toastr.error("Asegurese de no dejar campos vacios.", 'Error', {
                progressBar: true,
                closeButton: true,
                "timeOut": "5000",
            });
            return false
        }
        //Validar que no se entre valore negativos //
        if (seccionForm === seccionCampo[i].dataset.seccion && seccionCampo[i].value < 0) {
            toastr.error("No se admiten valores negativos.", 'Error', {
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
    for (var i = 0; i, i < campo.length; i++) {
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




//-------------------------PROCEDIMIENTO PARA GUARDAR LO VERIFICADO-------------------------------------//

$('form[name="formVerificacion"]').on('submit', function (e) {
    e.preventDefault();
    let seccion_form_verificacion = $(this).data('seccion');
    let listaIndIncluidos = $('select[name="indicadoresIncluidos"]');
    let id_seccion = $(this).data('id');

    if (validate_indicadores_no_empty(seccion_form_verificacion, listaIndIncluidos) === false) {
        return false
    }
    ;

    let campos = new FormData(this);

    campos.forEach(function (value, key) {
        console.log(key + ' : ' + value)
    });
    $.ajax({
        url: '/seccion/comprobacionInd/' + id_seccion + '/',
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
    if (element.length == 0) {
        return false
    }
}

const verificacionDeMenorAlTotalAReportar = (componenteTotalAreportar, componenteAcomparar) => {
    if (parseInt(componenteTotalAreportar.val()) < parseInt(componenteAcomparar.val())) {
        console.log(componenteTotalAreportar, componenteAcomparar)
        toastr.error("La cantidad de modelos " + componenteAcomparar.prop('name') + " debe ser menor que el " + componenteTotalAreportar.prop('name') + ".", 'Error', {
            progressBar: true,
            closeButton: true,
            "timeOut": "5000",
        });
        return false
    }
}

const validacionChecked = (element) => {
    if (element.is(':checked')) {
        console.log('checkeado')
    } else {
        toastr.error(element.prop('name') + " es requerido.", 'Error', {
            progressBar: true,
            closeButton: true,
            "timeOut": "5000",
        });
        return false;
    }
}

const validate_radios_no_empty = () => {
    let cod_pregunta_11 = $('.formCaptacion input[data-cod-pregunta="11"]');
    let cod_pregunta_13 = $('.formCaptacion input[data-cod-pregunta="13"]');
    let cod_pregunta_14 = $('.formCaptacion input[data-cod-pregunta="14"]');
    let cod_pregunta_15 = $('.formCaptacion input[data-cod-pregunta="15"]');
    let cod_pregunta_21 = $('.formCaptacion input[data-cod-pregunta="21"]');
    let cod_pregunta_22 = $('.formCaptacion input[data-cod-pregunta="22"]');
    let cod_pregunta_41 = $('.formCaptacion input[data-cod-pregunta="41"]');
    let cod_pregunta_51 = $('.formCaptacion input[data-cod-pregunta="51"]');
    let cod_pregunta_52 = $('.formCaptacion input[data-cod-pregunta="52"]');
    let cod_pregunta_53 = $('.formCaptacion input[data-cod-pregunta="53"]');
    let cod_pregunta_61 = $('.formCaptacion input[data-cod-pregunta="61"]');
    let cod_pregunta_71 = $('.formCaptacion input[data-cod-pregunta="71"]');
    let cod_pregunta_72 = $('.formCaptacion input[data-cod-pregunta="72"]');
    let cod_pregunta_73 = $('.formCaptacion input[data-cod-pregunta="73"]');
    let cod_pregunta_74 = $('.formCaptacion input[data-cod-pregunta="74"]');

    if (verificarExistencia(cod_pregunta_11) == false) {
        return false
    }
    ;
    if (validacionChecked(cod_pregunta_11) == false) {
        return false
    }
    ;

    if (verificarExistencia(cod_pregunta_13) == false) {
        return false
    }
    ;
    if (validacionChecked(cod_pregunta_13) == false) {
        return false
    }
    ;

    if (verificarExistencia(cod_pregunta_14) == false) {
        return false
    }
    ;
    if (validacionChecked(cod_pregunta_14) == false) {
        return false
    }
    ;

    if (verificarExistencia(cod_pregunta_15) == false) {
        return false
    }
    ;
    if (validacionChecked(cod_pregunta_15) == false) {
        return false
    }
    ;

    if (verificarExistencia(cod_pregunta_21) != false) {
        if (validacionChecked(cod_pregunta_21) == false) {
            return false
        }
        ;
    }
    ;

    if (verificarExistencia(cod_pregunta_22) != false) {
        if (validacionChecked(cod_pregunta_22) == false) {
            return false
        }
        ;
    }
    ;

    if (verificarExistencia(cod_pregunta_41) != false) {
        if (validacionChecked(cod_pregunta_41) == false) {
            return false
        }
        ;
    }
    ;

    if (verificarExistencia(cod_pregunta_51) != false) {
        if (validacionChecked(cod_pregunta_51) == false) {
            return false
        }
        ;
    }
    ;

    if (verificarExistencia(cod_pregunta_52) != false) {
        if (validacionChecked(cod_pregunta_52) == false) {
            return false
        }
        ;
    }
    ;
    if (verificarExistencia(cod_pregunta_53) != false) {
        if (validacionChecked(cod_pregunta_53) == false) {
            return false
        }
        ;
    }
    ;
    if (verificarExistencia(cod_pregunta_61) != false) {
        if (validacionChecked(cod_pregunta_61) == false) {
            return false
        }
        ;
    }
    ;
    if (verificarExistencia(cod_pregunta_71) != false) {
        if (validacionChecked(cod_pregunta_71) == false) {
            return false
        }
        ;
    }
    ;
    if (verificarExistencia(cod_pregunta_72) != false) {
        if (validacionChecked(cod_pregunta_72) == false) {
            return false
        }
        ;
    }
    ;
    if (verificarExistencia(cod_pregunta_73) != false) {
        if (validacionChecked(cod_pregunta_73) == false) {
            return false
        }
        ;
    }
    ;
    if (verificarExistencia(cod_pregunta_74) != false) {
        if (validacionChecked(cod_pregunta_74) == false) {
            return false
        }
        ;
    }
    ;


}

const validate_component_entero = (formulario) => {
    let claseForm = formulario.prop('class');

    let cod_pregunta_31 = $('.' + claseForm + ' input[data-cod-pregunta="31"]');
    let cod_pregunta_32 = $('.' + claseForm + ' input[data-cod-pregunta="32"]');
    let cod_pregunta_33 = $('.' + claseForm + ' input[data-cod-pregunta="33"]');
    let cod_pregunta_34 = $('.' + claseForm + ' input[data-cod-pregunta="34"]');
    let cod_pregunta_42 = $('.' + claseForm + ' input[data-cod-pregunta="42"]');
    let cod_pregunta_62 = $('.' + claseForm + ' input[data-cod-pregunta="62"]');
    let cod_pregunta_63 = $('.' + claseForm + ' input[data-cod-pregunta="63"]');

    let suma_modelos = parseInt(cod_pregunta_32.val()) + parseInt(cod_pregunta_33.val()) + parseInt(cod_pregunta_34.val())

    let arrayElement = [cod_pregunta_31, cod_pregunta_32, cod_pregunta_33, cod_pregunta_34, cod_pregunta_42, cod_pregunta_62, cod_pregunta_63];

    for (var i = 0; i < arrayElement.length; i++) {
        let verificacion = verificarExistencia(arrayElement[i]);
        if (verificacion != false) {
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
            if (verificacionDeMenorAlTotalAReportar(cod_pregunta_31, cod_pregunta_32) == false) {
                return false
            }
            ;
            if (verificacionDeMenorAlTotalAReportar(cod_pregunta_31, cod_pregunta_33) == false) {
                return false
            }
            ;
            if (verificacionDeMenorAlTotalAReportar(cod_pregunta_31, cod_pregunta_34) == false) {
                return false
            }
            ;
            if (parseInt(cod_pregunta_31.val()) !== suma_modelos) {
                toastr.error("El " + cod_pregunta_31.prop('name') + " no se corresponde con la suma entre: " + cod_pregunta_32.prop('name') + " " + cod_pregunta_33.prop('name') + " y " + cod_pregunta_34.prop('name') + ".", 'Error', {
                    progressBar: true,
                    closeButton: true,
                    "timeOut": "5000",
                });
                return false
            }
            if (parseInt(cod_pregunta_63.val()) > parseInt(cod_pregunta_62.val())) {
                toastr.error("La cantidad de establecimientos con contabilidad propia no " +
                    "puede ser mayor que la cantidad de establecimientos.", 'Error', {
                    progressBar: true,
                    closeButton: true,
                    "timeOut": "5000",
                });
                return false
            }
        }
    }
};

const validate_depedencias_campos = (formulario) => {
    let claseForm = formulario.prop('class');
    let cod_pregunta_11_No = $('.' + claseForm + ' input[data-cod-pregunta="11"]:input[value="No"] ');
    let cod_pregunta_11_Si = $('.' + claseForm + ' input[data-cod-pregunta="11"]:input[value="Si"] ');
    let cod_pregunta_12 = $('.' + claseForm + ' input[data-cod-pregunta="12"]');
    let cod_pregunta_13_No = $('.' + claseForm + ' input[data-cod-pregunta="13"]:input[value="No"] ');
    let cod_pregunta_13_Si = $('.' + claseForm + ' input[data-cod-pregunta="13"]:input[value="Si"] ');
    let cod_pregunta_14_Bueno = $('.' + claseForm + ' input[data-cod-pregunta="14"]:input[value="Bueno"] ');
    let cod_pregunta_14_Deteriorado = $('.' + claseForm + ' input[data-cod-pregunta="14"]:input[value="Deteriorado"] ');
    let cod_pregunta_14_No = $('.' + claseForm + ' input[data-cod-pregunta="14"]:input[value="No"] ');
    let cod_pregunta_15_No = $('.' + claseForm + ' input[data-cod-pregunta="15"]:input[value="No"] ');
    let cod_pregunta_15_Si = $('.' + claseForm + ' input[data-cod-pregunta="15"]:input[value="Si"] ');
    let cod_pregunta_41_No = $('.' + claseForm + ' input[data-cod-pregunta="41"]:input[value="No"] ');
    let cod_pregunta_41_Si = $('.' + claseForm + ' input[data-cod-pregunta="41"]:input[value="Si"] ');
    let cod_pregunta_21_No = $('.' + claseForm + ' input[data-cod-pregunta="21"]:input[value="No"] ');
    let cod_pregunta_21_Si = $('.' + claseForm + ' input[data-cod-pregunta="21"]:input[value="Si"] ');
    let cod_pregunta_22_No = $('.' + claseForm + ' input[data-cod-pregunta="22"]:input[value="No"] ');
    let cod_pregunta_22_Si = $('.' + claseForm + ' input[data-cod-pregunta="22"]:input[value="Si"] ');
    let cod_pregunta_42 = $('.' + claseForm + ' input[data-cod-pregunta="42"]');
    let cod_pregunta_52_No = $('.' + claseForm + ' input[data-cod-pregunta="52"]:input[value="No"] ');
    let cod_pregunta_52_Si = $('.' + claseForm + ' input[data-cod-pregunta="52"]:input[value="Si"] ');
    let cod_pregunta_53_Papel = $('.' + claseForm + ' input[data-cod-pregunta="53"]:input[value="Papel"] ');
    let cod_pregunta_53_Digital = $('.' + claseForm + ' input[data-cod-pregunta="53"]:input[value="Digital"] ');
    let cod_pregunta_53_No = $('.' + claseForm + ' input[data-cod-pregunta="53"]:input[value="No"] ');
    let cod_pregunta_61_No = $('.' + claseForm + ' input[data-cod-pregunta="61"]:input[value="No"] ');
    let cod_pregunta_61_Si = $('.' + claseForm + ' input[data-cod-pregunta="61"]:input[value="Si"] ');
    let cod_pregunta_62 = $('.' + claseForm + ' input[data-cod-pregunta="62"]');
    let cod_pregunta_63 = $('.' + claseForm + ' input[data-cod-pregunta="63"]');
    let cod_pregunta_71_No = $('.' + claseForm + ' input[data-cod-pregunta="71"]:input[value="No"] ');
    let cod_pregunta_71_Si = $('.' + claseForm + ' input[data-cod-pregunta="71"]:input[value="Si"] ');
    let cod_pregunta_711 = $('.' + claseForm + ' textarea[data-cod-pregunta="711"]');
    let cod_pregunta_72_No = $('.' + claseForm + ' input[data-cod-pregunta="72"]:input[value="No"] ');
    let cod_pregunta_72_Si = $('.' + claseForm + ' input[data-cod-pregunta="72"]:input[value="Si"] ');
    let cod_pregunta_721 = $('.' + claseForm + ' textarea[data-cod-pregunta="721"]');
    let cod_pregunta_73_No = $('.' + claseForm + ' input[data-cod-pregunta="73"]:input[value="No"] ');
    let cod_pregunta_73_Si = $('.' + claseForm + ' input[data-cod-pregunta="73"]:input[value="Si"] ');
    let cod_pregunta_731 = $('.' + claseForm + ' textarea[data-cod-pregunta="731"]');
    let cod_pregunta_74_No = $('.' + claseForm + ' input[data-cod-pregunta="74"]:input[value="No"] ');
    let cod_pregunta_74_Si = $('.' + claseForm + ' input[data-cod-pregunta="74"]:input[value="Si"] ');
    let cod_pregunta_741 = $('.' + claseForm + ' textarea[data-cod-pregunta="741"]');

    //--------DEPENDENCIAS PARA CUANDO SE CAPTA AL INICIO-----///
    if (claseForm == 'formCaptacion') {

        $('#14No').prop('hidden', true);
        $('#53No').prop('hidden', true);
        cod_pregunta_12.prop('readonly', true);
        cod_pregunta_13_No.prop('disabled', true).prop('checked', false);
        cod_pregunta_13_Si.prop('disabled', true).prop('checked', false);
        cod_pregunta_14_Bueno.prop('disabled', true).prop('checked', false);
        cod_pregunta_14_Deteriorado.prop('disabled', true).prop('checked', false);
        cod_pregunta_15_No.prop('disabled', true).prop('checked', false);
        cod_pregunta_15_Si.prop('disabled', true).prop('checked', false);
        cod_pregunta_22_No.prop('disabled', true).prop('checked', false);
        cod_pregunta_22_Si.prop('disabled', true).prop('checked', false);
        cod_pregunta_42.prop('readonly', true);
        cod_pregunta_62.prop('readonly', true);
        cod_pregunta_63.prop('readonly', true);
        cod_pregunta_711.prop('readonly', true).prop('value', "Ninguno");
        cod_pregunta_721.prop('readonly', true).prop('value', "");
        cod_pregunta_731.prop('readonly', true).prop('value', "");
        cod_pregunta_741.prop('readonly', true).prop('value', "");
    } else {
        //--------DEPENDENCIA PARA CUANDO SE EDITA LO CAPTADO-------//
        if (cod_pregunta_11_No.is(':checked')) {
            cod_pregunta_12.prop('readonly', true).prop('value', "No disponible");
            cod_pregunta_13_Si.prop('disabled', true);
            $('#14No').prop('hidden', false);
            cod_pregunta_14_No.prop('disabled', false).prop('checked', true);
            cod_pregunta_14_Bueno.prop('disabled', true);
            cod_pregunta_14_Deteriorado.prop('disabled', true);
            cod_pregunta_15_Si.prop('disabled', true);
        }
        if (cod_pregunta_52_No.is(':checked')) {
            $('#53No').prop('hidden', false);
            cod_pregunta_53_No.prop('disabled', false).prop('checked', true);
            cod_pregunta_53_Digital.prop('disabled', true);
            cod_pregunta_53_Papel.prop('disabled', true);
        }
        if (cod_pregunta_21_No.is(':checked')) {
            cod_pregunta_22_No.prop('disabled', false).prop('checked', true);
            cod_pregunta_22_Si.prop('disabled', true);
        }
        if (cod_pregunta_41_No.is(':checked')) {
            cod_pregunta_42.prop('readonly', true).prop('value', 0);
        }
        if (cod_pregunta_61_No.is(':checked')) {
            cod_pregunta_62.prop('readonly', true).prop('value', 0);
            cod_pregunta_63.prop('readonly', true).prop('value', 0);
        }
    }

    //DEPENDENCIA PARA AMBAS PARTE TANTO AL INICIO COMO AL EDITAR------//
    cod_pregunta_11_No.on('click', function () {
        cod_pregunta_12.prop('readonly', true).prop('value', "No disponible");
        cod_pregunta_13_No.prop('disabled', false).prop('checked', true);
        cod_pregunta_13_Si.prop('disabled', true);
        $('#14No').prop('hidden', false);
        cod_pregunta_14_No.prop('checked', true);
        cod_pregunta_14_Bueno.prop('disabled', true);
        cod_pregunta_14_Deteriorado.prop('disabled', true);
        cod_pregunta_15_No.prop('disabled', false).prop('checked', true);
        cod_pregunta_15_Si.prop('disabled', true);
    });
    cod_pregunta_11_Si.on('click', function () {
        cod_pregunta_12.prop('readonly', false);
        cod_pregunta_13_No.prop('disabled', false).prop('checked', false);
        cod_pregunta_13_Si.prop('disabled', false);
        $('#14No').prop('hidden', true);
        cod_pregunta_14_No.prop('checked', false);
        cod_pregunta_14_Bueno.prop('disabled', false).prop('checked', false);
        cod_pregunta_14_Deteriorado.prop('disabled', false);
        cod_pregunta_15_No.prop('disabled', false).prop('checked', false);
        cod_pregunta_15_Si.prop('disabled', false);
    });
    cod_pregunta_21_No.on('click', function () {
        cod_pregunta_22_No.prop('disabled', false).prop('checked', true);
        cod_pregunta_22_Si.prop('disabled', true);
    });
    cod_pregunta_21_Si.on('click', function () {
        cod_pregunta_22_No.prop('disabled', false).prop('checked', false);
        cod_pregunta_22_Si.prop('disabled', false).prop('checked', false);
    });
    cod_pregunta_41_No.on('click', function () {
        cod_pregunta_42.prop('readonly', true).prop('value', 0);
    });
    cod_pregunta_41_Si.on('click', function () {
        cod_pregunta_42.prop('readonly', false);
    });
    cod_pregunta_52_No.on('click', function () {
        $('#53No').prop('hidden', false);
        cod_pregunta_53_No.prop('checked', true);
        cod_pregunta_53_Papel.prop('disabled', true);
        cod_pregunta_53_Digital.prop('disabled', true);
    });
    cod_pregunta_52_Si.on('click', function () {
        $('#53No').prop('hidden', true);
        cod_pregunta_53_No.prop('checked', false);
        cod_pregunta_53_Papel.prop('disabled', false).prop('checked', false);
        cod_pregunta_53_Digital.prop('disabled', false);
    });
    cod_pregunta_61_No.on('click', function () {
        cod_pregunta_62.prop('readonly', true).prop('value', 0);
        cod_pregunta_63.prop('readonly', true).prop('value', 0);
    });
    cod_pregunta_61_Si.on('click', function () {
        cod_pregunta_62.prop('readonly', false);
        cod_pregunta_63.prop('readonly', false);
    });
    cod_pregunta_71_No.on('click', function () {
        cod_pregunta_711.prop('readonly', true).prop('value', "Ninguno");
        ;
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

const validateComponenteTexto = (formulario) => {
    let claseForm = formulario.prop('class');
    let texto = $('.' + claseForm + ' input[data-component="texto"]:text');
    for (var i = 0; i < texto.length; i++) {
        if (texto[i].dataset.type === "1" && texto[i].value === "") {
            toastr.error(texto[i].name + " es requerido.", 'Error', {
                progressBar: true,
                closeButton: true,
                "timeOut": "5000",
            });
            return false;
        } else {
            reg = /^[a-zA-ZñÑáéíóú_ ]+$/;
            if (!reg.test(texto[i].value)) {
                toastr.error(texto[i].name + " debe contener solo letras.", 'Error', {
                    progressBar: true,
                    closeButton: true,
                    "timeOut": "5000",
                });
                return false;
            }
        }
    }
}


//--------------------------------INICIALIZACION DE CAMPOS NUMERICOS EN SOBRE ENTIDAD--------------------------------//

let entero = $('.formCaptacion input[data-component="entero"]');
for (var i = 0; i < entero.length; i++) {
    entero[i].value = 0
}


//--------------------------------PROCEDIMIENTO PARA GUARDAR LO CAPTADO EN SOBRE ENTIDAD-----------------------------//


let formularioCaptacion = $('form[class="formCaptacion"]');

validate_depedencias_campos(formularioCaptacion);
formularioCaptacion.on('submit', function (e) {
    e.preventDefault();
    let campos = new FormData(this);

    if (validateComponenteTexto(formularioCaptacion) === false) {
        return false
    };
    if (validate_radios_no_empty() === false) {
        return false
    };
    if (validate_component_entero(formularioCaptacion) === false) {
        return false
    };
    campos.forEach(function (value, key) {
        console.log(key + ' : ' + value)
    });
    $.ajax({
        url: '/guia/dataCaptacion/',
        type: 'POST',
        data: campos,
        dataType: 'json',
        processData: false,
        contentType: false
    }).done(function (data) {
        if (data.hasOwnProperty('error')) {
            toastr.error(data.error, 'Error', {
                progressBar: true,
                closeButton: true,
                "timeOut": "5000",
            });
        } else {
            formularioCaptacion.trigger("reset")
            $('.desabilitar').removeClass("desabilitar");
            $('#cantCuestionario').load(' #cantCuestionario');
            toastr.success(data.exito, 'Exito', {
                progressBar: true,
                closeButton: true,
                "timeOut": "2000",
            });
        }
    }).fail(function (jqXHR, textStatus, errorThrown) {
        alert(textStatus + ' : ' + errorThrown)
    })
});


//-----------------------------------------PROCEDIMIENTO PARA GUARDAR LO CAPTADO EN EL FORM DE INSTANCIA--------------------------------------------------//

$('form[name="instanciaForm"]').on('submit', function (e) {
    e.preventDefault();
    let instancia_from_seccion = $(this).data('seccion');
    if (validateInstancias(instancia_from_seccion, $('select[name="seccion_id"]')) === false) {
        return false
    };
    if (validateInstancias(instancia_from_seccion, $('select[name="columna_id"]')) === false) {
        return false
    };
    if (validateInstancias(instancia_from_seccion, $('select[name="codigo_id"]')) === false) {
        return false
    };
    if (validateInstancias(instancia_from_seccion, $('input[name="modelo_1"]')) === false) {
        return false
    };
    if (validateInstancias(instancia_from_seccion, $('input[name="registro_1"]')) === false) {
        return false
    };
    if (validateInstancias(instancia_from_seccion, $('input[name="modelo_2"]')) === false) {
        return false
    };
    if (validateInstancias(instancia_from_seccion, $('input[name="registro_2"]')) === false) {
        return false
    };
    if (validateInstancias(instancia_from_seccion, $('input[name="modelo_3"]')) === false) {
        return false
    };
    if (validateInstancias(instancia_from_seccion, $('input[name="registro_3"]')) === false) {
        return false
    };
    let campos = new FormData(this);
    $.ajax({
        url: '/guia/dataCaptacion/',
        type: 'POST',
        data: campos,
        dataType: 'json',
        processData: false,
        contentType: false
    }).done(function (data) {
        toastr.success(data.sms, 'Exito', {
            progressBar: true,
            closeButton: true,
            "timeOut": "3000",
        });
        let modal = $('.instanciaModal');
        modal.modal('hide');
        $('button[name="actualizar"]').prop('disabled', false);
    }).fail(function (jqXHR, textStatus, errorThrown) {
        alert(textStatus + ' : ' + errorThrown)
    })
});

$('form[name="instanciaFormContuniarCaptacion"]').on('submit', function (e) {
    e.preventDefault();
    let instancia_from_seccion = $(this).data('seccion');
    let id = $(this).data('cuestionario');
    if (validateInstancias(instancia_from_seccion, $('select[name="seccion_id"]')) === false) {
        return false
    };
    if (validateInstancias(instancia_from_seccion, $('select[name="columna_id"]')) === false) {
        return false
    };
    if (validateInstancias(instancia_from_seccion, $('select[name="codigo_id"]')) === false) {
        return false
    };
    if (validateInstancias(instancia_from_seccion, $('input[name="modelo_1"]')) === false) {
        return false
    };
    if (validateInstancias(instancia_from_seccion, $('input[name="registro_1"]')) === false) {
        return false
    };
    if (validateInstancias(instancia_from_seccion, $('input[name="modelo_2"]')) === false) {
        return false
    };
    if (validateInstancias(instancia_from_seccion, $('input[name="registro_2"]')) === false) {
        return false
    };
    if (validateInstancias(instancia_from_seccion, $('input[name="modelo_3"]')) === false) {
        return false
    };
    if (validateInstancias(instancia_from_seccion, $('input[name="registro_3"]')) === false) {
        return false
    };
    let campos = new FormData(this);
    $.ajax({
        url: '/guia/continuarCaptacion/' + id + '/',
        type: 'POST',
        data: campos,
        dataType: 'json',
        processData: false,
        contentType: false
    }).done(function (data) {
        toastr.success(data.sms, 'Exito', {
            progressBar: true,
            closeButton: true,
            "timeOut": "5000",
        });
        let modal = $('.continuarCaptacionModal');
        modal.modal('hide');
        $('button[name="actualizar"]').prop('disabled', false);
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
    options += '<option value="' + id + '">' + nombre + '</option>';
    select.html(options)
});

let selectCol = $('select[name="columna_id"]');
$('select[name="seccion_id"]').on('change', function () {
    let id = $(this).val();
    $.ajax({
        url: '/seccion/getColumnas/',
        type: 'POST',
        data: {
            'action': 'getColumnas',
            'id': id
        },
        dataType: 'json'
    }).done(function (data) {
        if (!data.hasOwnProperty('error')) {
            selectCol.html('').select2({
                theme: "bootstrap4",
                language: 'es',
                data: data
            });
            return false
        }
    }).fail(function (jqXHR, textStatus, errorThrown) {
        alert(textStatus + ' : ' + errorThrown)
    });
});

let selectCod = $('select[name="codigo_id"]');
$('select[name="columna_id"]').on('change', function () {
    let columna_id = $(this).val();
    let options = '<option value="">---------</option>';
    if (columna_id === '') {
        selectCol.html(options)
    }
    $.ajax({
        url: '/seccion/getCodigos/',
        type: 'POST',
        data: {
            'action': 'getCodigos',
            'id': columna_id
        },
        dataType: 'json'
    }).done(function (data) {
        if (!data.hasOwnProperty('error')) {
            selectCod.html('').select2({
                theme: "bootstrap4",
                language: 'es',
                data: data
            });
            return false
        }
    }).fail(function (jqXHR, textStatus, errorThrown) {
        alert(textStatus + ' : ' + errorThrown)
    });
});





//----------------------------------------------PERSONALIZACION DE LA TABLA ENTIDAD------------------------------------------------------------------
$(document).ready(function () {

    $('#entidadTable tbody').on('click', 'a[rel="eliminarEntidad"]', function () {
        let tr = tblEntidad.cell($(this).closest('td, li')).index();
        let data = tblEntidad.row(':eq(' + tr.row + ')').data();
        notificacion('Notificacion', 'Estas seguro de eliminar al Centro Infomante (' + data.codigo_CI + '-' + data.nombre_CI + ').', function () {
            let url = 'http://scie.onei.gob.cu/entidad/eliminarEntidad/' + data.id + '/';
            location.href = url
        });
    });


    // -----------------------------------------------CREACION DE FILTROS POR CADA COLUMNA-----------------------------------------

    $('#entidadTable thead tr').clone(true).appendTo('#entidadTable thead');

    $('#entidadTable thead tr:eq(1) th').each(function (i) {
        var title = $(this).text();
        $(this).html('<input type="text" id="' + title + '1" placeholder="' + title + '" style="border-color: blue;border-top:0px;border-left:0px;border-right: 0px; width: 100%"/>');

        $('input', this).on('keyup change ', function () {
            if (tblEntidad.column(i).search() !== this.value) {
                tblEntidad
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
        for (var i = 0; i < selector.length; i++) {
            array.push(tblEntidad.rows('.selected').data()[i]);
        }
        if (array.length === 0) {
            toastr.error("Seleccione al menos una opcion para conformar el universo.", 'Error', {
                progressBar: true,
                closeButton: true,
                "timeOut": "3000",
            });
            return false
        } else {
            let listaEnitdadesSelected = JSON.stringify(array);
            $.ajax({
                url: '/guia/universo/',
                type: 'POST',
                data: {
                    'action': 'crearUniverso',
                    'data': listaEnitdadesSelected
                },
                dataType: 'json'
            }).done(function (data) {
                toastr.success(data.exito, 'Exito', {
                    progressBar: true,
                    closeButton: true,
                    "timeOut": "3000",
                });
            }).fail(function (jqXHR, textStatus, errorThrown) {
                toastr.error(textStatus + ' : ' + errorThrown, 'Error', {
                    progressBar: true,
                    closeButton: true,
                    "timeOut": "3000",
                })
            });
        }
    });

    //---------------------PROCEDIMIENTO PARA ELIMINAR TODAS LAS ENTIDADES SELECTED--------------------------//
    $('#eliminarCIselected').on('click', function () {
        let selector = $('.selected');
        let array = [];
        for (var i = 0; i < selector.length; i++) {
            array.push(tblEntidad.rows('.selected').data()[i]);
        }
        if (array.length === 0) {
            toastr.error("Debe seleccionar al menos una opcion.", 'Error', {
                progressBar: true,
                closeButton: true,
                "timeOut": "3000",
            });
            return false
        } else {
            let listaEnitdadesSelected = JSON.stringify(array);
            $.ajax({
                url: '/entidad/eliminarCIselected/',
                type: 'POST',
                data: {
                    'action': 'eliminarCIselected',
                    'data': listaEnitdadesSelected
                },
                dataType: 'json'
            }).done(function (data) {
                if (data.hasOwnProperty('error')) {
                    toastr.error(data.error, 'Error', {
                        progressBar: true,
                        closeButton: true,
                        "timeOut": "5000",
                    });
                } else {
                     tblEntidad.ajax.reload(toastr.success(data.exito, 'Exito', {
                    progressBar: true,
                    closeButton: true,
                    "timeOut": "3000",
                }), false)
                }
            }).fail(function (jqXHR, textStatus, errorThrown) {
                toastr.error(textStatus + ' : ' + errorThrown, 'Error', {
                    progressBar: true,
                    closeButton: true,
                    "timeOut": "3000",
                })
            });
        }
    });
});


$('div[data-model-name="modal"]').on('shown.bs.modal', function () {
    $('form[name="instanciaForm"]').trigger("reset")
});

//------------------------------------------------PARTE PARA MOSTRAR LO CAPTADO---------------------------------------//
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
            if (data[i].pregunta != null) {
                informacion += '<h6 class="text-bold text-uppercase">' + '<span class="badge bg-gradient-primary" style="width: 100%; padding: 10px">' + data[i].pregunta + '</span>' + '</h6>' + '<h6 class="text-bold text-center text-uppercase" >' + data[i].respuesta + '</h6>' + '<hr>'

            }
        }
        let table = '<table class="table table-hover table-striped" >' +
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
                table += '<tr><td>' + '<span class="badge bg-gradient-navy" style="padding: 3px">' + data[i].seccion_id + '</span>' + '</td>' +
                    '<td>' + data[i].codigo_id + '</td>' +
                    '<td>' + data[i].columna_id + '</td>' +
                    '<td>' + data[i].modelo_1 + '</td>' +
                    '<td>' + data[i].registro_1 + '</td>' +
                    '<td>' + '<span class="badge bg-gradient-navy" style="padding: 3px">' + data[i].diferencia_1 + '</span>' + '</td>' +
                    '<td>' + data[i].modelo_2 + '</td>' +
                    '<td>' + data[i].registro_2 + '</td>' +
                    '<td>' + '<span class="badge bg-gradient-navy" style="padding: 3px">' + data[i].diferencia_2 + '</span>' + '</td>' +
                    '<td>' + data[i].modelo_3 + '</td>' +
                    '<td>' + data[i].registro_3 + '</td>' +
                    '<td>' + '<span class="badge bg-gradient-navy" style="padding: 3px">' + data[i].diferencia_3 + '</span></td></tr>'
            }
        }
        table += '</tbody></table>'
        contenido.html(informacion + table);
    }).fail(function (jqXHR, textStatus, errorThrown) {
        alert(textStatus + ' : ' + errorThrown)
    });
});


//--------------------------------MODIFICACIONES DE LAS COSAS CAPTADAS DEL CUESTIONARIO---------------------------------------------//


//----------PROCEDIMIENTO PARA VALIDAR Y MODIFICAR LAS PREGUNTAS ---------//

let formularioEditarCaptacion = $('form[class="editFormCaptacion"]');

validate_depedencias_campos(formularioEditarCaptacion);
formularioEditarCaptacion.on('submit', function (e) {
    e.preventDefault();
    let campos = new FormData(this);
    if (validateComponenteTexto(formularioEditarCaptacion) === false) {
        return false
    }
    ;
    if (validate_component_entero(formularioEditarCaptacion) === false) {
        return false
    }
    ;

    envioConAjax(window.location.pathname, 'Notificación', '¿Estás seguro de realizar esta acción?', campos, function () {
        let url = 'http://scie.onei.gob.cu/guia/guiaCaptada/';
        location.href = url
    });

});

//-----------PROCEDIMIENTO PARA VALIDAR Y MODIFICAR LAS INSTANCIAS---------------//
$('form[name="editarInstanciaForm"]').on('submit', function (e) {
    e.preventDefault();
    let instanciaSeccion = $(this).data('seccion');
    let modal = $('#modalEditarInstancia'+instanciaSeccion);
    if (validateInstancias(instanciaSeccion, $('input[name="1_modelo"]')) === false) {return false};
    if (validateInstancias(instanciaSeccion, $('input[name="1_registro"]')) === false) {return false};
    if (validateInstancias(instanciaSeccion, $('input[name="2_modelo"]')) === false) {return false};
    if (validateInstancias(instanciaSeccion, $('input[name="2_registro"]')) === false) {return false};
    if (validateInstancias(instanciaSeccion, $('input[name="3_modelo"]')) === false) {return false};
    if (validateInstancias(instanciaSeccion, $('input[name="3_registro"]')) === false) {return false};
    let campos = new FormData(this);
    $.ajax({
        url: '/seccion/editarInstancia/',
        type: 'POST',
        data: campos,
        dataType: 'json',
        processData: false,
        contentType: false
    }).done(function (data) {
        modal.modal('hide');
        window.location.reload()
    }).fail(function (jqXHR, textStatus, errorThrown) {
        alert(textStatus + ' : ' + errorThrown)
    })
});

$('.acordeon').on('click', function () {
    console.log($('.registro'))
    $('.formVerificacion').prop('hidden', true);
    let seccionAcordion = $(this).data('seccion');
    for (var i = 0; i, i < $('.registro').length; i++) {
        if (seccionAcordion === $('.registro')[i].dataset.seccionRegistro && $('.registro')[i].textContent !== "") {
            $('.formVerificacion').prop('hidden', false)
        }
    }
});




//-------------------------------VALIDACIONES DENTRO DE LOS FORMULARIOS DENTRO DE LA SECCION ADMIN--------------------------//

$('#guiaForm').bootstrapValidator({
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

$('#entidadForm').bootstrapValidator({
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

$('#periodoForm').bootstrapValidator({
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

$('#seccionForm').bootstrapValidator({
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
            validators: {
                notEmpty: {
                    message: 'Campo requerido. Debe seleccionar una opcion'
                },

            }
        },
        numero: {
            message: 'El numero no es valido',
            validators: {
                regexp: {
                    regexp: /^[0-9]+$/,
                    message: 'Solo se admiten digitos.'
                }
            }
        },
        subNumero: {
            message: 'El subNumero no es valido',
            validators: {
                regexp: {
                    regexp: /^[0-9]+$/,
                    message: 'Solo se admiten digitos.'
                }
            }
        },
        orden: {
            message: 'El orden no es valido',
            validators: {
                notEmpty: {
                    message: 'El orden es requerido'
                },
                regexp: {
                    regexp: /^[0-9]+$/,
                    message: 'Solo se admiten digitos.'
                }
            }
        },
        tipo: {
            validators: {
                notEmpty: {
                    message: 'Campo requerido. Debe seleccionar una opcion'
                },

            }
        }


    }
});

//---------------MOSTRAR TEXTO DE AYUDA DE LOS CAMPOS DEL SSECCION-FORM QUE LO TENGAN-------//
$('#campoOrden').on('mouseover', function () {
        $('#textoAyudaOrden').prop('hidden', false);
});
$('#campoOrden').on('click', function () {
        $('#textoAyudaOrden').prop('hidden', true);
});

$('#campoNombre').on('mouseover', function () {
        $('#textoAyudaNombre').prop('hidden', false);
});
$('#campoNombre').on('click', function () {
        $('#textoAyudaNombre').prop('hidden', true);
});

$('#select2-campoTipo-container').on('mouseover', function () {
        $('#textoAyudaTipo').prop('hidden', false);
});
$('#select2-campoTipo-container').on('click', function () {
        $('#textoAyudaTipo').prop('hidden', true);
});


$('#codigoForm').bootstrapValidator({
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

$('#columnaForm').bootstrapValidator({
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

$('#clasificadorIndForm').bootstrapValidator({
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
                    regexp: /^[a-zA-ZñÑáéíóú()_ ]+$/,
                    message: 'Solo se admiten letras'
                }

            }
        },

    }
});

$('#indicadoresForm').bootstrapValidator({
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
                    regexp: /^[a-zA-ZñÑáéíóú0-9?._ ]+$/,
                    message: 'Solo se admiten letras'
                }

            }
        },

    }
});

$('#respuestasForm').bootstrapValidator({
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
                    callback: function (value, validator) {
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
        groups: {
            message: 'El nombre no es valido',
            validators: {
                notEmpty: {
                    message: 'Debe de seleccionar una opcion'
                },
            }
        },
    }
});





//------------------PROCEDIMIENTO PARA CREAR UNA GUIA CON LAS MISMAS CONFIGURACIONES DE OTRA YA DEFINIDA-----------------------//
const url = () => {
    location.href = 'http://scie.onei.gob.cu/guia/listarGuias/';
}
guias = $('#listadoGuiasDefinidas');
buttonSafe = $('#safe');
checkboxGuias = $('#guiasDefinidas');
salvadoNormal = $('#salvadoNormal');

checkboxGuias.on('click', function () {
    if (checkboxGuias.is(':checked') == true) {
        guias.prop('disabled', false);
        buttonSafe.prop('disabled', false);
        salvadoNormal.prop('disabled', true)

    } else {
        guias.prop('disabled', true);
        buttonSafe.prop('disabled', true);
        salvadoNormal.prop('disabled', false)
    }
});

$('#safe').on('click', function () {
    guiaNombre = $('#guiaNombre');
    guiaActiva = $('#guiaActiva');
    if (guias.val() === guiaNombre.val()) {
        toastr.error("El nombre de la guia a crear ya existe.", 'Error', {
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
            'action': 'creacionDeGuia',
            'guiaNueva': guiaNombre.val(),
            'guiaYaDefinida': guias.val(),
            'activo': guiaActiva[0].checked
        },
        dataType: 'json',
    }).done(function (data) {
        toastr.success(data.exito, 'Exito', {
            progressBar: true,
            closeButton: true,
            "timeOut": "1500",
        });
        setTimeout(url, 1500);
    }).fail(function (jqXHR, textStatus, errorThrown) {
        alert(textStatus + ' : ' + errorThrown)
    })

})



//---------------------------------PROCEDIMIENTO PARA El REPORTE DE VERIFICACION--------------------------------------//
$('#reporteVerificacionGeneral').DataTable({
    dom: "Bfrtip",
    buttons: {
        dom: {
            button: {
                className: 'boton-salvar btn1'
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

$('#tblVerificacionPorProvincia').DataTable({
    scrollX: true,
    dom: "Bfrtip",
    buttons: {
        dom: {
            button: {
                className: 'boton-salvar btn1'
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



//--------------------------------------PROCEDIMIENTO PARA El REPORTE GENERAL---------------------------------------------//
$('#reporteGeneral').DataTable({
    scrollX: true,
    dom: "Bfrtip",
    buttons: {
        dom: {
            button: {
                className: 'boton-salvar btn1'
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



//--------------------------PROCEDIMIENTO PARA El REPORTE DE DISCIPLINA INFORMATIVA----------------------------------//
$('#reporteDisciplinaInfo').DataTable({
    dom: "Bfrtip",
    buttons: {
        dom: {
            button: {
                className: 'boton-salvar btn1'
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



//---------------------------------PROCEDIMIENTO PARA El REPORTE DE SEÑALAMIENTO DE ERRORES-----------------------------//
$('#reporteErrores').DataTable({
    dom: "Bfrtip",
    buttons: {
        dom: {
            button: {
                className: 'boton-salvar btn1'
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



//---------------------------PROCEDIMIENTO PARA El REPORTE DE Displina info Centro Controlado-----------------------------//
$('#reporteDisciplinaInfoCentroControlados').DataTable({
    dom: "Bfrtip",
    buttons: {
        dom: {
            button: {
                className: 'boton-salvar btn1'
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



//------------------------------PROCEDIMIENTO PARA El REPORTE DE Domicilio Social Incorrecto-----------------------------//
$('#reporteDomicilioSocial').DataTable({
    dom: "Bfrtip",
    buttons: {
        dom: {
            button: {
                className: 'boton-salvar btn1'
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



//---------------------------------PROCEDIMIENTO PARA El REPORTE DE DEFICIENCIAS-----------------------------//
$('#reporteDeficiencias').DataTable({
    dom: "Bfrtip",
    buttons: {
        dom: {
            button: {
                className: 'boton-salvar btn1'
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



//---------------------------------PROCEDIMIENTO PARA El REPORTE DE CAPTACION-----------------------------//
$('#tblCaptado').DataTable({});

$('#tblNoCaptado').DataTable({});



//---------------------------------PROCEDIMIENTO PARA MANDAR A REALIZAR LAS IMPORTACIONES--------------------------------//

const importar = (formulario, url) => {

    formulario.on('submit', function (e) {
        e.preventDefault();
        let campos = new FormData(this);
        $.ajax({
            url: url,
            type: 'POST',
            data: campos,
            dataType: 'json',
            processData: false,
            contentType: false
        }).done(function (data) {
            if (data.hasOwnProperty('error')) {
                toastr.error(data.error, 'Error', {
                    progressBar: true,
                    closeButton: true,
                    "timeOut": "5000",
                });
            } else {
                tblEntidad.ajax.reload(toastr.success(data.exito, 'Exito', {
                    progressBar: true,
                    closeButton: true,
                    "timeOut": "3000",
                }), false)

            }

        }).fail(function (jqXHR, textStatus, errorThrown) {
            alert(textStatus + ' : ' + errorThrown)
        })
    })
};

                                 //-----------PARA ENTIDAD-----------//
let formImportarCI = $('form[name="formImportarCI"]');
importar(formImportarCI,'/entidad/importarEntidad/');

                                //-----------PARA NAE-----------//
let formImportarNAE = $('form[name="formImportarNAE"]');
importar(formImportarNAE,'/entidad/importarNAE/');

                                //-----------PARA OSDE-----------//
let formImportarOsde = $('form[name="formImportarOsde"]');
importar(formImportarOsde,'/entidad/importarOSDE/');

                                //-----------PARA ORGANISMO-----------//
let formImportarOrganismo = $('form[name="formImportarOrganismo"]');
importar(formImportarOrganismo,'/entidad/importarORG/');
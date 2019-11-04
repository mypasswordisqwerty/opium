$(() => {
    let backtime = 0;

    function msg(m, cls = 'danger') {
        const err = jQuery("<div/>").addClass(`alert alert-${cls}`).text(m);
        err.appendTo($('#errors'));
        setTimeout(() => {
            err.remove();
        }, 5000);
    }

    function call(data, callback) {
        $.getJSON({
            url: '/q',
            method: 'POST',
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify(data)
        }).done((json) => {
            if (json.error) {
                msg(json.error)
                return;
            }
            callback(json);
        }).fail((xhr, err, thrown) => {
            msg(thrown);
        });
    }

    function subBack(){
        backtime-=1;
        $("#addback").text('+30 sec' + (backtime>0 ? ` (${backtime}) ` : ''));
        if (backtime>0){
            setTimeout(subBack, 1200);
        }
    }

    function updState(json) {
        if (backtime<=0 && json.backtime>0){
            setTimeout(subBack, 1200);
        }
        backtime = json.backtime;
        $("#back").removeClass("btn-success btn-danger").addClass(json.back ? 'btn-danger' : 'btn-success');
        $("#back").text(json.back ? 'Выключить' : 'Включить')
        $("#addback").removeClass("btn-success btn-danger").addClass(json.back ? 'btn-danger' : 'btn-success');
        $("#addback").text('+30 sec' + (backtime>0 ? `(${backtime})` : ''));
        $("#fore").removeClass("btn-success btn-danger").addClass(json.fore ? 'btn-danger' : 'btn-success');
        $("#fore").text(json.fore ? 'Выключить' : 'Включить')
        $("#light").removeClass("btn-success btn-danger").addClass(json.light ? 'btn-danger' : 'btn-success');
        $("#light").text(json.light ? 'Выключить' : 'Включить')
        $("#door").text(json.door ? 'Закрыто' : 'Открыто')
        $("#door").removeClass("badge-success badge-danger").addClass(json.door ? 'badge-success' : 'badge-danger');
        $("#gate").text(json.gate ? 'Закрыто' : 'Открыто')
        $("#gate").removeClass("badge-success badge-danger").addClass(json.gate ? 'badge-success' : 'badge-danger');
        $("#lsens").text(json.lsens);
        if (json.time_start) {
            $("#time_start").text(json.time_start);
        }
        if (json.time_end) {
            $("#time_end").text(json.time_end);
        }
        let cfg = json.conf;
        for (let i = 1; i <= 3; i++) {
            $("#l" + i).prop('checked', cfg & 1);
            cfg >>= 1;
        }
    }



    $("#fore").click(() => {
        call({ fore: 1 }, updState);
    });

    $("#addback").click(() => {
        call({ addback: 1 }, updState);
    });
    $("#back").click(() => {
        call({ back: 1 }, updState);
    });

    $("#light").click(() => {
        call({ light: 1 }, updState);
    });
    $("#l1,#l2,#l3").change(() => {
        let cfg = 0;
        for (let i = 3; i >= 1; i--) {
            cfg <<= 1;
            cfg |= $("#l" + i).prop('checked') ? 1 : 0;
        }
        call({ conf: cfg }, updState);
    });

    call({ getconf: 0 }, updState);
    setInterval(() => {
        call({ data: 0 }, updState);
    }, 5000);

});

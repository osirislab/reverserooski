function createForm(o) {
    let tr = $(o).closest('tr');
    let form = $('<form method="POST"></form>');
    form.append(tr.find('input[name="id"]'));
    let hidden_csrf = $('<input type="hidden" name="csrf_token"/>');
    hidden_csrf.val(csrf_token.value);
    form.append(hidden_csrf);
    return form;
}

function render_client(data) {
    let pending_list = $('.pending-list')[0];
    let finished_list = $('.finished-list')[0];

    for (int i=0; i<data['pending'].length; ++i) {
        pending_list.append(
            $(`<li>$( data['pending'][i] )</li>`)
        );
    }

};

$(document).ready(function() {
    $(".client-select").click(function() {
        this.class += "btn-primary";
        let clientid = this.id;
        console.log(this);
        $.get(`/client/getinfo/${ clientid }`, function(data) {
            render_client(data);
        });
    });
});

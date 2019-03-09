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
    
};

$(document).ready(function() {
    $(".client-select").click(function() {
        this.class += "btn-primary";
        console.log(this);
        $.post('/client/data', data={
            clientid: this.id
        }, function(data) {
            render_client(data);
        });
    });
});

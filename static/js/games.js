$(function(){
    var url = '/games'
    $("#grid").dxDataGrid({
        dataSource: DevExpress.data.AspNet.createStore({
            key: "id",
            loadUrl: url,
            insertUrl: url,
            updateUrl: url,
            deleteUrl: url,
            onBeforeSend: function(method, ajaxOptions) {
                ajaxOptions.xhrFields = { withCredentials: true };
            }
        }),

        editing: {
            allowUpdating: true,
            allowDeleting: true,
            allowAdding: true
        },

        paging: {
            pageSize: 50
        },

        pager: {
            showPageSizeSelector: false,
            allowedPageSizes: [8, 12, 20]
        },

        columns: [{
            dataField: "id",
            dataType: "number",
            allowEditing: false
        }, {
            dataField: "title"
        }, {
            dataField: "description"
        }, {
            dataField: "category"
        }, {
            dataField: "trailer"
        }, {
            dataField: "version"
        }, {
            dataField: "company"
        },{
            dataField: "price",
            dataType: "number"
        },{
            dataField: "quantity",
            dataType: "number"
        },{
            dataField: "valoration",
            dataType: "number"
        }, ],
    }).dxDataGrid("instance");
});

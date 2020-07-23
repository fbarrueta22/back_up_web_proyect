$(function(){
  $.getJSON("/users", function (dataUsers){
    $.getJSON("/games", function (dataGames){
      var url = '/reviews'
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
              dataField: "content"
          }, {
              dataField: "write_on",
              dataType: "datetime",
              allowEditing: false
          }, {
              dataField: "valoration",
              dataType: "number"
          },{
              dataField: "user_id",
              dataType: "number",
              allowEditing: false,
              visible: false
          }, {
              dataField: "user",
              lookup: {
                dataSource: dataUsers,
                valueExpr: 'username',
                displayExpr: 'username',
                placeholder: 'Select username'
              }
          },{
              dataField: "game_id",
              dataType: "number",
              allowEditing: false,
              visible: false
          },{
              dataField: "game",
              lookup: {
                dataSource: dataGames,
                valueExpr: 'title',
                displayExpr: 'title',
                placeholder: 'Select title'
              }
          }, ],
      }).dxDataGrid("instance");
    });
  });
});

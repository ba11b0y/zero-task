
const TABLE_HEADER = `<tr class="header">
<th>NAME</th>
<th>OPEN</th>
<th>HIGH</th>
<th>LOW</th>
<th>CLOSE</th>
<th>PREVIOUS CLOSE</th>
<th>NUMBER OF TRADES</th>
</tr>`

function f(element) {
    console.log(element);
    $(".results").empty();
    $.ajax({
        url: `https://${window.location.hostname}/details?scrip_name=` + element,
        type: 'GET',
        dataType: 'json',
        success: function (result) {
            let res = result.res;
            $(".details-table").show().empty();
            $(".details-table").append(TABLE_HEADER);
            $(".details-table").append(`<tr>
                <td>${element}</td>
                <td>${res["OPEN"]}</td>
                <td>${res["HIGH"]}</td>
                <td>${res["LOW"]}</td>
                <td>${res["CLOSE"]}</td>
                <td>${res["PREVCLOSE"]}</td>
                <td>${res["TRADES"]}</td>
                 
            `);
        }
    })
        .fail((error) => {
            console.log("Error: ", error);
        });
}

const makeInitTable = () => {

    $(".details-table").empty();
    $(".details-table").append(TABLE_HEADER);

    $.ajax({
        type: 'GET',
        url: `https://${window.location.hostname}/fetch`,
        dataType: 'json',
        success: function (results) {


            for (var result in results) {
                console.log(result);
                $(".details-table").append(`<tr>
                <td>${result}</td>
                <td>${results[result].OPEN}</td>
                <td>${results[result].HIGH}</td>
                <td>${results[result].LOW}</td>
                <td>${results[result].CLOSE}</td>
                <td>${results[result].PREVCLOSE}</td>
                <td>${results[result].TRADES}</td>

            `);
            }

        }
    })
        .fail((error) => {
            console.log("Error: ", error);
        });



}

$(document).ready(() => {

    makeInitTable();

    $(".search-field").keyup((event) => {
        event.preventDefault();
        let query = $(".search-field").val();
        $(".details-table").hide();

        $.ajax({
            url: `https://${window.location.hostname}/search?query=` + query,
            type: 'GET',
            dataType: 'json',
            success: function (result) {
                console.log('result! -->', result);
                $(".results").empty();
                let results = result.res.slice(0, 10);

                results.forEach(element => {
                    $(".results").append(`<li><div onclick="f(\'${element}\')">${element}</div></li>`);
                });

            }
        })
            .fail((error) => {
                console.log("Error: ", error);
            });
    });

});

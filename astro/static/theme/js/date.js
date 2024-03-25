function set_birthday_date(selection) {

        var date = new Date(selection['date']);
alert(date);
        var dateOptions = { day: '2-digit', month: '2-digit', year: 'numeric' };
        var currentDate = date.toLocaleDateString('ja-JP', dateOptions).replace(/\//gi, '-');
        var timeOptions = { hour: '2-digit', minute: '2-digit' };
        var currentTime = date.toLocaleTimeString('it-IT', timeOptions);

        document.getElementById('time').value = currentTime;
        document.getElementById("date").valueAsDate = date

}

function set_date(id_date, id_time, date_iso) {

    var date = new Date(date_iso);
    var timeOptions = { hour: '2-digit', minute: '2-digit' , second: '2-digit' };
    document.getElementById(id_time).value = date.toLocaleTimeString(timeOptions);

    const dateForDateTimeInputValue = new Date(date.getTime() + new Date().getTimezoneOffset() * -60 * 1000);

    document.getElementById(id_date).valueAsDate = dateForDateTimeInputValue;
}


//function set_new_date(value) {
//
//   var old_date = document.getElementById("id_transit_date").value
//   var str_date = value + old_date.substring(10, 16)
//   var date = new Date(str_date);
//   document.getElementById("id_transit_date").text = date.isoformat()
//
//}
//
//function set_new_time(value) {
//
//   var old_date = document.getElementById("date").value
//   var str_date = old_date.substring(0, 11) + value
//   var date = new Date(str_date);
//   document.getElementById("id_transit_date").text = date.isoformat()
//
//}

//function update_new_transit_date(object) {
//
//   var str_date = document.getElementById("date").value
//   var str_time = document.getElementById("time").value
//   alert(str_date);
//   alert(str_time);
//   var str_transit_date = old_date.substring(0, 11) + value
//   var date = new Date(str_date);
//   document.getElementById("id_transit_date").text = date.isoformat()
//
//}

//function set_default_transit_date(id_transit_date, id_transit_time, id_a_transit_date) {
//
//        var date = new Date();
//
//        var dateOptions = { day: '2-digit', month: '2-digit', year: 'numeric' };
//        var currentDate = date.toLocaleDateString('ja-JP', dateOptions).replace(/\//gi, '-');
//        var timeOptions = { hour: '2-digit', minute: '2-digit' };
//        var currentTime = date.toLocaleTimeString('it-IT', timeOptions);
//
//        document.getElementById(id_transit_time).value = currentTime;
//        console.log(date);
//        document.getElementById(id_transit_date).valueAsDate = date;
//        document.getElementById(id_a_transit_date).textContent = date.getUTCDate();
//
////        $("#id_a_transit_date").text(date);
//}

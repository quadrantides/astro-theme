//function load_transit(theme_id, date) {
//
//  var location = "/theme/transit/" + theme_id + "/" + date;
//  window.location = location;
//}

function update_transit_date(id_form, id_transit_date, id_transit_time, utc_transit_date_iso)  {

    alert(utc_transit_date_iso);
  set_transit_date(id_transit_date, id_transit_time, utc_transit_date_iso) ;
  $('#id-new-transit-form').submit()

}

function set_transit_date(id_transit_date, id_transit_time, utc_transit_date_iso) {

    var utc_date = new Date(utc_transit_date_iso);
    var timeOptions = { hour: '2-digit', minute: '2-digit' , second: '2-digit' };
    document.getElementById(id_transit_time).value = utc_date.toLocaleTimeString(timeOptions);

    const dateForDateTimeInputValue = new Date(utc_date.getTime() + new Date().getTimezoneOffset() * -60 * 1000);

    document.getElementById(id_transit_date).valueAsDate = dateForDateTimeInputValue;
}

var Moments = (function () {
    "use strict";

    var dates = [];

    function _refresh_date(date) {
        date.html(moment(date.attr("data-date")).fromNow());
    }

    function _refresh_dates() {
        for (var i = 0; i < dates.length; i++)
            _refresh_date(dates[i]);
        setTimeout(_refresh_dates, 60000)
    }

    function _relative_date(date) {
        _refresh_date(date);
        return dates.push(date);
    }

    _refresh_dates();

    return {
        relative_date: _relative_date
    }
})();
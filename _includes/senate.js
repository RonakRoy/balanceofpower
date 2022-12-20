const election_type = "senate";

function caucuses_with(party, senator) {
    if (party in caucus_map) {
        return caucus_map[party];
    }
    else if (party == "Independent" && (senator=="Bernie Sanders" || senator=="Angus King" || senator=="Harry F. Byrd Jr.")) {
        return "Democratic";
    }
    else {
        return party;
    }
}

$("g.outer").hover(function(e) {
    state = abbr_map[$(this).attr("id")];

    $('#info-box').css('display','block');
    $('#info-box').find("#state_name").html(state);
    $('#info-box').find('#races').html("");

    if (!(state in data[year])) {
        $('#info-box').find('#races').html(
            "<div class='race'>" + 
                "<div class='race-type'>no election in " + year + "</div>" +
            "</div>"
        );
    }
    else {
        for (const seat_class in data[year][state]) {
            const race_element = $("<div class='race'></div>");

            const type = (data[year][state][seat_class]["special"] ? "special" : "regular") + " class " + seat_class + " election"
            race_element.append("<div class='race-type'>" + type + "</div>");

            const race_data = data[year][state][seat_class];

            if (race_data["percentage"]) {
                var winner_check = "<img src='/assets/images/check.svg'></img>";
                for (const c in race_data["candidate"]) {
                    const inc_class = (race_data["candidate"][c]==race_data["before"]["senator"]) ? " inc" : "";
                    race_element.append(
                        "<div class='candidate" + inc_class + "'>" +
                            "<div class='color " + party_class(race_data["party"][c]) + "'>" + winner_check + "</div>" +
                            "<div class='name'>" + race_data["candidate"][c] + "</div>" +
                            "<div class='party'>" + race_data["party"][c] + "</div>" + 
                            "<div class='percent'>" + race_data["percentage"][c] + "</div>" + 
                            "<div class='votes'>" + race_data["votes"][c] + "</div>" + 
                        "</div>"
                    );

                    winner_check = "";
                }

                const old_caucus = caucuses_with(race_data["before"]["party"], race_data["before"]["senator"]);
                const new_caucus = caucuses_with(race_data["party"][0], race_data["candidate"][0])
                var outcome = new_caucus + " hold.";
                if (old_caucus != new_caucus) {
                    var outcome = "<b>" + new_caucus + " pickup.</b>";
                }
                race_element.append("<div class='party-outcome'>" + outcome + "</div>");
            }
            else {
                for (const c in race_data["candidate"]) {
                    const inc_class = (race_data["candidate"][c]==race_data["before"]["senator"]) ? " inc" : "";
                    race_element.append(
                        "<div class='candidate" + inc_class + "'>" +
                            "<div class='color " + party_class(race_data["party"][c]) + "'></div>" +
                            "<div class='name'>" + race_data["candidate"][c] + "</div>" +
                            "<div class='party'>" + race_data["party"][c] + "</div>" + 
                        "</div>"
                    );
                }
                race_element.append("<div class='party-outcome'>Forwarded to January Runoff.</div>");
            }

            $('#info-box').find('#races').append(race_element);
        }
    }
});

function update_map_and_info() {
    var type;
    if (year % 2 == 0) {
        var election_class = (year/2 % 3);
        if (election_class==0) election_class = 3;
        type = "Class " + election_class + " elections and";
    }
    else {
        type = "Off-year";
    }
    $('#year_info').find('#type').html(type + " special elections.");

    var up = {"Democratic":0, "Republican":0};
    var pickup = {"Democratic":0, "Republican":0};

    for (const state in data[year]) {
        const group_state =  $("#" + name_map[state]);
        const main_state =  $("#" + name_map[state] + "_main");
        const secondary_state = $("#" + name_map[state] + "_secondary");
        
        var secondary = false;
        for (const seat_class in data[year][state]) {
            const seat_data = data[year][state][seat_class];

            const state_object = (secondary) ? secondary_state : main_state;

            if (seat_data["percentage"]) {
                state_object.addClass(party_class(seat_data["party"][0]));

                const old_caucus = caucuses_with(seat_data["before"]["party"], seat_data["before"]["senator"]);
                const new_caucus = caucuses_with(seat_data["party"][0], seat_data["candidate"][0])

                up[old_caucus] += 1;

                if (old_caucus!=new_caucus) {
                    pickup[new_caucus] += 1;

                    const striped_state = state_object.clone();
                    striped_state.addClass("striped");
                    group_state.append(striped_state);
                    if (!secondary) group_state.append(secondary_state);
                    group_state.append(group_state.find("text"));
                }
            }
            else {
                state_object.addClass("runoff");
            }

            secondary = true;
        }
    }

    for (const party in up) {
        $('#' + party + '-up').html(up[party]);
        $('#' + party + '-pickup').html(pickup[party]);
    }
}
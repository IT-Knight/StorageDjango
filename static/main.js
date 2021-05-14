function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', function() {

    Array.from(document.querySelectorAll('div.interface_block')).slice(1).forEach((row) => {
        row.onmouseover = () => {
            row.style.backgroundColor = '#F3F3F3';
            let divs = row.children;
            let delete_btn = divs[divs.length - 1];
            delete_btn.style.visibility = 'visible'
        }
        row.onmouseout = () => {
            row.style.backgroundColor = '#FFFFFF';
            let divs = row.children;
            let delete_btn = divs[divs.length - 1];
            delete_btn.style.visibility = 'hidden'
        }
        row.ontouchstart = () => {
            row.style.backgroundColor = '#F3F3F3';
        }
        row.ontouchend = () => {
            row.style.backgroundColor = '#FFFFFF';
        }
    });


    // upload handler
    document.querySelectorAll('input[type="file"]').forEach(input => {
        input.addEventListener('change', (event) => {

            if (input.files.length > 0) {
                document.querySelector('span.drop-zone__prompt').style.display = 'none';
                document.querySelector('#drop_zone_file_list1').style.display = 'block';

            } else {
                document.querySelector('span.drop-zone__prompt').style.display = 'unset';
                document.querySelector('#drop_zone_file_list1').style.display = 'none';
            }

            if (input.files.length > 20) {
                document.querySelector('#drop_zone_file_list1').style.overflow = "scroll";
            }

            let str_filelist = '';
            let html_text = '';
            for (var i = 1; i < input.files.length + 1; ++i) {
                let file_name = input.files.item(i-1).name
                str_filelist = str_filelist + `${i}. ` + file_name + '\n';
                html_text = html_text + `<div class="file_row">${i}. ${file_name}</div>`
            }
            console.log(str_filelist)
            const upload_file_list_block1 = document.querySelector('#drop_zone_file_list1')
            const upload_file_list_block2 = document.querySelector('#drop_zone_file_list2')
            upload_file_list_block1.innerHTML = html_text
            // upload_file_list_block2.innerHTML = html_text


        })
    });
    document.querySelectorAll('#upload_files_form').forEach(form => {
        form.onsubmit = () => {
            document.querySelector('#drop_zone_file_list1').style.overflow = "unset"
            document.querySelector('#drop_zone_file_list1').innerHTML = 'Uploading...'
            document.querySelector('#drop_zone_file_list2').innerHTML = 'Uploading...'
            // close_upload_popup()
        }
    })

    if (document.querySelectorAll('#action_log_block div.action_table_row').length > 16) {
            document.querySelectorAll('.pre_event_table').forEach(element => {
               element.style.overflow = "scroll";
            })
    } else {
        document.querySelectorAll('.pre_event_table').forEach(element => {
               element.style.overflow = "unset";
        })
    }
    // ----------------------------------------------------------------------------

    //match width handlers.
    window.matchMedia('(min-width:931px)').addEventListener('change', () => {
        document.querySelectorAll('.item-a').forEach(item => {
            let title = item.getAttribute('title')
            if (item.textContent.length < 35 && title && title.length > 25) {
                item.textContent = title.slice(0, 38) + "..."
                if (item.textContent.length > title.length) {
                    item.textContent = title
                }
            }
        })
    });

    window.matchMedia('(min-width:481px), (max-width: 930px)').addEventListener('change', () => {
        document.querySelectorAll('.item-a').forEach(item => {
            let title = item.getAttribute('title')
            console.log(item)
            if ((item.textContent.length > 31) || (item.textContent.length < 26 && title && title.length > 24)) {
                item.textContent = item.textContent.slice(0,31) + "..." // 34

                if (item.textContent.length > title.length) {
                    item.textContent = title
                }
            }
        })
    });

    window.matchMedia('(min-width:321px), (max-width: 480px)').addEventListener('change', () => {
        document.querySelectorAll('.item-a').forEach(item => {

            let title = item.getAttribute('title')
            if ((item.textContent.length > 33 && title) || (item.textContent.length < 23 && title && title > 22)) {
                item.textContent = title.slice(0,35) + "..."
                if (item.textContent.length > title.length) {
                    item.textContent = title
                }
            }
        })
    });

    window.matchMedia('(max-width: 320px)').addEventListener('change', () => {
        document.querySelectorAll('.item-a').forEach(item => {
            let title = item.getAttribute('title')
            if (item.textContent.length > 24 && title) {
                item.textContent = title.slice(0,22) + "..." //25
            }
        })
    });

});

function open_upload_popup() {
    document.querySelector('#upload_popup').className = 'show';
    document.querySelector('#drop_zone_file_list1').style.overflow = "unset";
}

function close_upload_popup() {
    document.querySelector('#upload_popup').className = 'hidden';
    document.querySelector('#upload_files_form').reset();
    if (document.querySelector(`div.drop-zone__thumb`)) {
        document.querySelector('div.drop-zone__thumb').remove()
    }
    document.querySelector(".drop-zone__prompt").style.display = 'unset';
    document.querySelector('#drop_zone_file_list1').innerHTML = null;

}


function open_actionlogs_popup() {
    document.querySelector('#action_log_block').className = 'show';
    document.querySelector('#action_log_block2').className = 'show';
}

function close_actionlogs_popup() {
    document.querySelector('#action_log_block').className = 'hidden';
    document.querySelector('#action_log_block2').className = 'hidden';
}

function open_createdir_popup() {
    document.querySelector('#create_dir_block').className = 'show';
    document.querySelector('#create_dir_block2').className = 'show';
}
function close_createdir_popup() {
    document.querySelector('#create_dir_block').className = 'hidden';
    document.querySelector('#create_dir_block2').className = 'hidden';
}

function clear_log(webpath) {
    fetch(`/delete_logs/${webpath}`)
        .then(response => {
            console.log(response)
            console.log(response.status)
            location.reload()
        });
}

function delete_process(object_webpath, data_id, objname) {
    const csrftoken = getCookie('csrftoken');
    let the_div = document.querySelector(`div[data-id="${data_id}"]`)
    let type = the_div.getAttribute('data-type')
    console.log(object_webpath)
    if (type === 'folder') {
        var result = confirm(`Are you sure you want to delete this directory and all it's content?\n/${objname}`);
    } else {
        var result = confirm(`Are you sure you want to delete this file?\n${objname}`);
    }
    if (result) {
        fetch(`/delete/${data_id}`)
        .then(response => {
            console.log(response)
            console.log(response.status)
            if (response.status === 204) {
                document.querySelector(`div[data-id="${data_id}"]`).remove();
            } else {
                alert('Oops, something went wrong. Please refresh the page and try one more time')
            }
        })
    }

}
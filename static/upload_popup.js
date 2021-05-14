document.querySelectorAll(".drop-zone__input").forEach((inputElement) => {
  const dropZoneElement = inputElement.closest(".drop-zone");

  dropZoneElement.addEventListener("click", (e) => {
    inputElement.click();
  });

  inputElement.addEventListener("change", (e) => {
    if (inputElement.files.length) {
      // updateThumbnail(dropZoneElement, inputElement.files[0]);
    }
  });

  dropZoneElement.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZoneElement.classList.add("drop-zone--over");
  });

  ["dragleave", "dragend"].forEach((type) => {
    dropZoneElement.addEventListener(type, (e) => {
      dropZoneElement.classList.remove("drop-zone--over");
      console.log('--over removed1')
    });
  });

  dropZoneElement.addEventListener("drop", (e) => {
    e.stopPropagation();
      e.preventDefault();

    dropZoneElement.classList.remove("drop-zone--over");
    console.log('--over removed2')


    if (e.dataTransfer.files.length) {
        inputElement.files = e.dataTransfer.files;

        document.querySelector('span.drop-zone__prompt').style.display = 'none';
        document.querySelector('#drop_zone_file_list1').style.display = 'block';
        if (inputElement.files.length > 20) {
            document.querySelector('#drop_zone_file_list1').style.overflow = "scroll";
        }
        const upload_file_list_block1 = document.querySelector('#drop_zone_file_list1')
        let str_filelist = '';
        let html_text = '';
        for (var i = 1; i < inputElement.files.length + 1; ++i) {
            let file = inputElement.files.item(i-1);
            if (!file.type && file.size % 4096 === 0 && !file.name.endsWith('.msi') && !file.name.endsWith(".parts")) {
                // console.log(inputElement.files.item(i-1).name)
                document.querySelector('#drop_zone_file_list1').style.overflow = "unset";
                upload_file_list_block1.innerHTML = "You can upload only files. Please exclude folders and try again!"
                return false
            }
            let file_name = inputElement.files.item(i-1).name
            str_filelist = str_filelist + `${i}. ` + file_name + '\n';
            html_text = html_text + `<div class="file_row">${i}. ${file_name}</div>`
        }
        console.log(str_filelist)
        const upload_file_list_block2 = document.querySelector('#drop_zone_file_list2')
        upload_file_list_block1.innerHTML = html_text
        // upload_file_list_block2.innerHTML = html_text
    }

  });
});

/**
 * Updates the thumbnail on a drop zone element.
 *
 * @param {HTMLElement} dropZoneElement
 * @param {File} file
 */
function updateThumbnail(dropZoneElement, file) {
  let thumbnailElement = dropZoneElement.querySelector(".drop-zone__thumb");

  // First time - remove the prompt
  if (dropZoneElement.querySelector(".drop-zone__prompt")) {
    dropZoneElement.querySelector(".drop-zone__prompt").style.display = 'none';
  }

  // First time - there is no thumbnail element, so lets create it
  if (!thumbnailElement) {
    thumbnailElement = document.createElement("div");
    thumbnailElement.classList.add("drop-zone__thumb");
    dropZoneElement.appendChild(thumbnailElement);
  }

  thumbnailElement.dataset.label = file.name;

  // Show thumbnail for image files
  if (file.type.startsWith("image/")) {
    const reader = new FileReader();

    reader.readAsDataURL(file);
    reader.onload = () => {
      thumbnailElement.style.backgroundImage = `url('${reader.result}')`;
    };
  } else {
    thumbnailElement.style.backgroundImage = null;
  }
}

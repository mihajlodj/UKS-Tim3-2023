import api from '../api'

const fileToBase64 = (fileUrl) => {
	return new Promise((resolve, reject) => {
		const xhr = new XMLHttpRequest();
		xhr.onload = function () {
			const reader = new FileReader();
			reader.onloadend = function () {
				resolve(reader.result);
			}
			reader.onerror = function (error) {
				reject(error);
			}
			reader.readAsDataURL(xhr.response);
		};
		xhr.onerror = function (error) {
			reject(error);
		};
		xhr.open('GET', fileUrl);
		xhr.responseType = 'blob';
		xhr.send();
	});
}

const uploadFiles = (files, username, repoName, data) => {
    let filePromises = files.map(file => {
        return fileToBase64(file["url"]).then(base64String => {
            return {
                "name": file["file"]["name"],
                "content": base64String.split("base64,")[1]
            };
        }).catch(error => {
            console.error('Error:', error);
        });
    });

    return Promise.all(filePromises)
        .then(fileData => {
            data["files"] = fileData;
            return api.post(`/repository/upload/${username}/${repoName}/`, data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
};


export default { uploadFiles }
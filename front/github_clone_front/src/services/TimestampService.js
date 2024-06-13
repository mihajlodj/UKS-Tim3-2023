const howLongAgo = (timestamp) => {
    const currentDate = new Date();
    try {
        const previousDate = new Date(timestamp);
     
    
    console.log("PREV DATE:");
    console.log(previousDate);
    console.log(timestamp);
    const seconds = Math.floor((currentDate - previousDate) / 1000);
    let interval = Math.floor(seconds / 31536000);

    if (interval >= 1) {
        return interval + " year" + (interval === 1 ? "" : "s") + " ago";
    }
    interval = Math.floor(seconds / 2592000);
    if (interval >= 1) {
        return interval + " month" + (interval === 1 ? "" : "s") + " ago";
    }
    interval = Math.floor(seconds / 86400);
    if (interval >= 1) {
        return interval + " day" + (interval === 1 ? "" : "s") + " ago";
    }
    interval = Math.floor(seconds / 3600);
    if (interval >= 1) {
        return interval + " hour" + (interval === 1 ? "" : "s") + " ago";
    }
    interval = Math.floor(seconds / 60);
    if (interval >= 1) {
        return interval + " minute" + (interval === 1 ? "" : "s") + " ago";
    }
    return Math.floor(seconds) + " second" + (Math.floor(seconds) === 1 ? "" : "s") + " ago";
}
    catch {
        console.log("AAAAA");
        console.log(timestamp);
        return "aaa";
    }
}

export default {howLongAgo}
// Tự động lấy URL base từ window.location
const getBaseUrl = () => {
    const protocol = window.location.protocol;
    const host = window.location.host;
    return `${protocol}//${host}`;
};

const BASE_URL = getBaseUrl();

// Các API endpoint
const API_WS = `ws://${window.location.host}/ws`;
const API_CHART = `ws://${window.location.host}/ws`;

const API_REGISTER = `${BASE_URL}/api/register`;
const API_LOGIN = `${BASE_URL}/api/login`;
const API_CHAT = `${BASE_URL}/api/chat`;

const API_PREDICT_RISK = `${BASE_URL}/api/predict-flood-risk`;

const API_TOGGLE_SENSOR = `${BASE_URL}/api/sensor/toggle`;
const API_GET_SENSOR_STATUS = `${BASE_URL}/api/sensor/status`;
const API_SET_DISTANCE_SENSOR = `${BASE_URL}/api/sensor/water-level`;

const API_LOGIN_STATE = `${BASE_URL}/api/user/login-state`;
const API_GET_USER_LIST = `${BASE_URL}/api/user/list`;

const API_ADMIN_AUTH = `${BASE_URL}/api/admin/auth`;
const API_ADMIN_PASS = `${BASE_URL}/api/admin/password`;
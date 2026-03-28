/**
 * Curated icon registry mapping string names to react-icons components.
 * Used by components (e.g. Timeline) to render icons specified from Python by name.
 *
 * Includes popular icons from Font Awesome 5 (fa) and Material Design (md).
 * Emoji strings are handled separately at the component level.
 */
import { IconType } from "react-icons";

// Font Awesome 5 (solid)
import {
  FaCheck, FaTimes, FaPlus, FaMinus, FaUser, FaUsers, FaHome, FaCog, FaBell, FaEnvelope,
  FaPhone, FaSearch, FaStar, FaHeart, FaThumbsUp, FaThumbsDown, FaEdit, FaTrash, FaSave, FaLock,
  FaUnlock, FaEye, FaEyeSlash, FaUpload, FaDownload, FaFile, FaFolder, FaImage, FaCamera, FaVideo,
  FaMusic, FaMapMarkerAlt, FaClock, FaCalendar, FaCalendarCheck, FaCalendarPlus, FaCalendarMinus,
  FaShoppingCart, FaCreditCard, FaMoneyBillWave, FaTruck, FaPlane, FaCar, FaBicycle, FaWalking,
  FaRocket, FaGlobe, FaCloud, FaSun, FaMoon, FaBolt, FaFire, FaSnowflake, FaLeaf,
  FaChartLine, FaChartBar, FaChartPie, FaDatabase, FaServer, FaLaptop, FaMobileAlt, FaDesktop,
  FaCode, FaBug, FaRobot, FaComments, FaComment, FaPaperPlane, FaBookmark, FaTag, FaTags,
  FaFlag, FaTrophy, FaMedal, FaGraduationCap, FaBriefcase, FaBuilding, FaHospital, FaAmbulance,
  FaShieldAlt, FaKey, FaLink, FaExternalLinkAlt, FaShareAlt, FaCopy, FaClipboard,
  FaInfoCircle, FaExclamationCircle, FaExclamationTriangle, FaQuestionCircle, FaCheckCircle, FaTimesCircle,
  FaArrowUp, FaArrowDown, FaArrowLeft, FaArrowRight, FaChevronUp, FaChevronDown, FaChevronLeft, FaChevronRight,
  FaSpinner, FaSync, FaBan, FaPause, FaPlay, FaStop, FaStepForward, FaStepBackward,
  FaWifi, FaBatteryFull, FaPrint, FaQrcode, FaBarcode, FaFingerprint, FaMicrophone, FaHeadphones,
  FaPalette, FaPaintBrush, FaPen, FaEraser, FaRuler, FaDraftingCompass, FaCut, FaPaste,
  FaBox, FaBoxOpen, FaArchive, FaWarehouse, FaDollarSign, FaPercent, FaReceipt,
  FaUserPlus, FaUserMinus, FaUserCheck, FaUserShield, FaUserTie, FaUserCog,
  FaHandshake, FaGavel, FaBalanceScale, FaCertificate, FaAward, FaCrown,
  FaHammer, FaWrench, FaScrewdriver, FaToolbox, FaPlug, FaPowerOff,
  FaGithub, FaTwitter, FaLinkedin, FaSlack, FaDocker, FaPython, FaReact, FaNodeJs, FaAws,
} from "react-icons/fa";

// Material Design
import {
  MdHome, MdSearch, MdSettings, MdNotifications, MdEmail, MdPhone, MdPerson, MdGroup,
  MdStar, MdFavorite, MdThumbUp, MdThumbDown, MdEdit, MdDelete, MdSave, MdLock,
  MdVisibility, MdVisibilityOff, MdCloudUpload, MdCloudDownload, MdFolder, MdImage,
  MdVideoCall, MdLocationOn, MdAccessTime, MdEvent, MdShoppingCart, MdCreditCard,
  MdLocalShipping, MdFlight, MdDirectionsCar, MdDirectionsBike, MdDirectionsWalk,
  MdRocketLaunch, MdPublic, MdCloud, MdWbSunny, MdNightsStay, MdFlashOn, MdWhatshot,
  MdShowChart, MdBarChart, MdPieChart, MdStorage, MdComputer, MdSmartphone, MdDesktopWindows,
  MdCode, MdBugReport, MdChat, MdSend, MdBookmark, MdLabel, MdFlag,
  MdInfo, MdError, MdWarning, MdHelp, MdCheckCircle, MdCancel,
  MdArrowUpward, MdArrowDownward, MdArrowBack, MdArrowForward, MdExpandLess, MdExpandMore,
  MdCheck, MdClose, MdAdd, MdRemove,
  MdDashboard, MdAnalytics, MdTimeline, MdAccountTree, MdWorkspaces,
} from "react-icons/md";

export const iconRegistry: Record<string, IconType> = {
  // Font Awesome 5 (solid)
  FaCheck, FaTimes, FaPlus, FaMinus, FaUser, FaUsers, FaHome, FaCog, FaBell, FaEnvelope,
  FaPhone, FaSearch, FaStar, FaHeart, FaThumbsUp, FaThumbsDown, FaEdit, FaTrash, FaSave, FaLock,
  FaUnlock, FaEye, FaEyeSlash, FaUpload, FaDownload, FaFile, FaFolder, FaImage, FaCamera, FaVideo,
  FaMusic, FaMapMarkerAlt, FaClock, FaCalendar, FaCalendarCheck, FaCalendarPlus, FaCalendarMinus,
  FaShoppingCart, FaCreditCard, FaMoneyBillWave, FaTruck, FaPlane, FaCar, FaBicycle, FaWalking,
  FaRocket, FaGlobe, FaCloud, FaSun, FaMoon, FaBolt, FaFire, FaSnowflake, FaLeaf,
  FaChartLine, FaChartBar, FaChartPie, FaDatabase, FaServer, FaLaptop, FaMobileAlt, FaDesktop,
  FaCode, FaBug, FaRobot, FaComments, FaComment, FaPaperPlane, FaBookmark, FaTag, FaTags,
  FaFlag, FaTrophy, FaMedal, FaGraduationCap, FaBriefcase, FaBuilding, FaHospital, FaAmbulance,
  FaShieldAlt, FaKey, FaLink, FaExternalLinkAlt, FaShareAlt, FaCopy, FaClipboard,
  FaInfoCircle, FaExclamationCircle, FaExclamationTriangle, FaQuestionCircle, FaCheckCircle, FaTimesCircle,
  FaArrowUp, FaArrowDown, FaArrowLeft, FaArrowRight, FaChevronUp, FaChevronDown, FaChevronLeft, FaChevronRight,
  FaSpinner, FaSync, FaBan, FaPause, FaPlay, FaStop, FaStepForward, FaStepBackward,
  FaWifi, FaBatteryFull, FaPrint, FaQrcode, FaBarcode, FaFingerprint, FaMicrophone, FaHeadphones,
  FaPalette, FaPaintBrush, FaPen, FaEraser, FaRuler, FaDraftingCompass, FaCut, FaPaste,
  FaBox, FaBoxOpen, FaArchive, FaWarehouse, FaDollarSign, FaPercent, FaReceipt,
  FaUserPlus, FaUserMinus, FaUserCheck, FaUserShield, FaUserTie, FaUserCog,
  FaHandshake, FaGavel, FaBalanceScale, FaCertificate, FaAward, FaCrown,
  FaHammer, FaWrench, FaScrewdriver, FaToolbox, FaPlug, FaPowerOff,
  FaGithub, FaTwitter, FaLinkedin, FaSlack, FaDocker, FaPython, FaReact, FaNodeJs, FaAws,

  // Material Design
  MdHome, MdSearch, MdSettings, MdNotifications, MdEmail, MdPhone, MdPerson, MdGroup,
  MdStar, MdFavorite, MdThumbUp, MdThumbDown, MdEdit, MdDelete, MdSave, MdLock,
  MdVisibility, MdVisibilityOff, MdCloudUpload, MdCloudDownload, MdFolder, MdImage,
  MdVideoCall, MdLocationOn, MdAccessTime, MdEvent, MdShoppingCart, MdCreditCard,
  MdLocalShipping, MdFlight, MdDirectionsCar, MdDirectionsBike, MdDirectionsWalk,
  MdRocketLaunch, MdPublic, MdCloud, MdWbSunny, MdNightsStay, MdFlashOn, MdWhatshot,
  MdShowChart, MdBarChart, MdPieChart, MdStorage, MdComputer, MdSmartphone, MdDesktopWindows,
  MdCode, MdBugReport, MdChat, MdSend, MdBookmark, MdLabel, MdFlag,
  MdInfo, MdError, MdWarning, MdHelp, MdCheckCircle, MdCancel,
  MdArrowUpward, MdArrowDownward, MdArrowBack, MdArrowForward, MdExpandLess, MdExpandMore,
  MdCheck, MdClose, MdAdd, MdRemove,
  MdDashboard, MdAnalytics, MdTimeline, MdAccountTree, MdWorkspaces,
};

/**
 * Look up an icon by name. Returns the IconType component or undefined.
 * Falls back to undefined if name is not in the registry (caller should
 * handle emoji/text fallback).
 */
export function getIcon(name: string): IconType | undefined {
  return iconRegistry[name];
}

/**
 * Get all available icon names (useful for documentation).
 */
export function getAvailableIconNames(): string[] {
  return Object.keys(iconRegistry);
}

import { MODAL_COLORS, MODAL_ICONS } from '../config/constants'
import type { ModalType } from '../types'

interface ModalProps {
    isOpen: boolean
    onClose: () => void
    title: string
    message: string
    type: ModalType
}

export function Modal({ isOpen, onClose, title, message, type }: ModalProps) {
    if (!isOpen) return null

    return (
        <div
            className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm"
            onClick={onClose}
        >
            <div
                className="bg-white rounded-2xl shadow-2xl max-w-md w-full mx-4 overflow-hidden transform transition-all duration-300 scale-100"
                onClick={(e) => e.stopPropagation()}
            >
                <div className={`bg-gradient-to-r ${MODAL_COLORS[type]} p-6 text-white`}>
                    <div className="flex items-center gap-3">
                        <span className="text-4xl">{MODAL_ICONS[type]}</span>
                        <h3 className="text-2xl font-bold">{title}</h3>
                    </div>
                </div>
                <div className="p-6">
                    <p className="text-gray-700 text-lg whitespace-pre-line leading-relaxed">{message}</p>
                </div>
                <div className="p-6 pt-0 flex justify-end">
                    <button
                        onClick={onClose}
                        className="px-8 py-3 bg-gradient-to-r from-purple-600 to-indigo-600 text-white font-bold rounded-xl hover:from-purple-700 hover:to-indigo-700 transform hover:scale-105 transition-all duration-200 shadow-lg"
                    >
                        OK
                    </button>
                </div>
            </div>
        </div>
    )
}

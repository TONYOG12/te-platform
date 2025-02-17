import { ExclamationCircleIcon } from '@heroicons/react/20/solid'


export const FormSelect = ({ field, label, data, handleInputChange, value, required }) => {

    return (
        <div className=''>
            <label
                htmlFor={field}
                className="block text-sm font-medium leading-6 text-sky-800"
            >
                {label}
            </label>

            <div className="mt-2">
                <select
                    name={field}
                    id={field}
                    className="block w-full rounded-md border-0 py-1.5  shadow-sm ring-1 ring-inset ring-gray-300  focus:ring-sky-600 sm:text-sm sm:leading-6"
                    defaultValue={value}
                    onChange={(e) => handleInputChange({ field: field, value: e.target.value })}
                    required={required}
                >
                    <option value=""></option>
                    {data.map((item) => (
                        <option key={item} value={item}>{item}</option>
                    ))}
                </select>
            </div>
        </div>

    )
}


export const FormInputWithValidation = ({ type, label, field, placeholder, handleInputChange, validation, value, required }) => {
    return (
        <div className="relative mt-2 rounded-md shadow-sm">
            <label
                htmlFor={field}
                className="block text-sm font-medium leading-6 text-sky-800"
            >
                {label}
            </label>
            <input
                type={type ?? "text"}
                name={field}
                id={field}
                placeholder={placeholder}
                defaultValue={value ?? ""}
                className="block w-full rounded-md border-0 px-1.5 py-1.5  shadow-sm ring-1 ring-inset ring-gray-300  focus:ring-sky-600 sm:text-sm sm:leading-6"
                aria-invalid={validation}
                onChange={(e) => handleInputChange({ field: field, value: e.target.value })}
                required={required}
            />
            {validation &&
                <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-3">
                    <ExclamationCircleIcon className="h-5 w-5 text-red-500" />
                </div>
            }
        </div>
    )
}

export const TextArea = ({ label, field, handleInputChange }) => {
    return (
        <div>
            <label
                htmlFor="notes"
                className="block text-sm font-medium leading-6 text-sky-800"
            >
                {label}
            </label>
            <div className="mt-2">
                <textarea
                    id={field}
                    name={field}
                    rows={4}
                    className="block w-full rounded-md border-0 py-1.5  shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-sky-600 sm:text-sm sm:leading-6"
                    defaultValue={''}
                    onChange={(e) => handleInputChange({ field: field, value: e.target.value })}
                />
            </div>
        </div>
    )
}
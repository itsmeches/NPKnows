import { Disclosure } from "@headlessui/react";
import { ChevronUpIcon } from "@heroicons/react/24/solid";
import React from "react";

const Accordion = ({ title, children }) => {
  return (
    <div className="w-full my-2">
      <Disclosure>
        {({ open }) => (
          <>
            <Disclosure.Button className="flex w-full justify-between rounded-lg bg-blue-100 px-4 py-2 text-left text-blue-900 font-medium hover:bg-blue-200 focus:outline-none focus-visible:ring focus-visible:ring-blue-500 focus-visible:ring-opacity-75">
              <span>{title}</span>
              <ChevronUpIcon
                className={`${open ? "rotate-180 transform" : ""} h-5 w-5 text-blue-500`}
              />
            </Disclosure.Button>
            <Disclosure.Panel className="px-4 pt-2 pb-2 text-gray-700">
              {children}
            </Disclosure.Panel>
          </>
        )}
      </Disclosure>
    </div>
  );
};

export default Accordion;

import snakeCase from "lodash/snakeCase";

export const snakeToCamel = (obj) => {
  const toCamel = (str) =>
    str.replace(/_([a-z])/g, (_, letter) => letter.toUpperCase());

  if (Array.isArray(obj)) {
    return obj.map((item) => snakeToCamel(item));
  } else if (obj !== null && typeof obj === "object") {
    return Object.keys(obj).reduce((acc, key) => {
      const camelKey = toCamel(key);
      acc[camelKey] = snakeToCamel(obj[key]); // Recursively handle nested objects/arrays
      return acc;
    }, {});
  }
  return obj; // Return the value if it's not an object or array
};

export const camelToSnake = (obj) => {
  const newObj = {};
  for (const key in obj) {
    if (Object.prototype.hasOwnProperty.call(obj, key)) {
      const newKey = key.replace(/([A-Z])/g, "_$1").toLowerCase();
      newObj[newKey] = obj[key];
    }
  }
  return newObj;
};

export const prepareFormData = (form) => {
  return {
    ...form,
    question_group: form?.question_group
      ?.map((qg) => snakeToCamel(qg))
      ?.map((qg) => ({
        ...qg,
        question: qg?.question?.map((q) => snakeToCamel(q)),
      })),
  };
};

export const prepareFormSubmission = (form) => {
  return {
    ...form,
    question_group: form?.question_group
      ?.map((qg) => camelToSnake(qg))
      ?.map((qg) => ({
        ...qg,
        name: qg?.name || snakeCase(qg?.label),
        question: qg?.question
          ?.map((q) => camelToSnake(q))
          .map((q) => ({
            ...q,
            name: q?.name || snakeCase(q?.label),
          })),
      })),
  };
};

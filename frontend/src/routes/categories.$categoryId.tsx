import {
  Box,
  Button,
  FormControl,
  FormErrorMessage,
  FormLabel,
  Heading,
  Input,
  Select,
  Spinner,
  Text,
  Textarea,
  VStack,
} from "@chakra-ui/react"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { createFileRoute, useNavigate } from "@tanstack/react-router"
import { useForm } from "react-hook-form"

import {
  type ApiError,
  type CategoryPublic,
  type CategoryUpdate,
  CategoriesService,
} from "@/client"
import useCustomToast from "@/hooks/useCustomToast"

export const Route = createFileRoute("/categories/$categoryId")({
  component: Category,
})

function Category() {
  const { categoryId } = Route.useParams()
  const queryClient = useQueryClient()
  const showToast = useCustomToast()
  const navigate = useNavigate()

  const { data: category, isLoading: isCategoryLoading } = useQuery<
    CategoryPublic,
    ApiError
  >({
    queryKey: ["categories", categoryId],
    queryFn: () => CategoriesService.readCategory({ id: categoryId }),
  })

  const { data: allCategories, isLoading: areAllCategoriesLoading } = useQuery<
    CategoryPublic[],
    ApiError
  >({
    queryKey: ["categories"],
    queryFn: async () => (await CategoriesService.readCategories({})).data,
  })

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<CategoryUpdate>({
    mode: "onBlur",
    criteriaMode: "all",
    values: category,
  })

  const mutation = useMutation({
    mutationFn: (data: CategoryUpdate) =>
      CategoriesService.updateCategory({ id: categoryId, requestBody: data }),
    onSuccess: () => {
      showToast("Success!", "Category updated successfully.", "success")
      queryClient.invalidateQueries({ queryKey: ["categories"] })
      navigate({ to: "/categories" })
    },
    onError: (err: ApiError) => {
      const errDetail = (err.body as any)?.detail
      showToast("Something went wrong.", `${errDetail}`, "error")
    },
  })

  const onSubmit = (data: CategoryUpdate) => {
    mutation.mutate(data)
  }

  const getDescendants = (
    catId: string,
    categories: CategoryPublic[],
  ): string[] => {
    const children = categories.filter((c) => c.parent_category_id === catId)
    let descendants = children.map((c) => c.id)
    children.forEach((child) => {
      descendants = [...descendants, ...getDescendants(child.id, categories)]
    })
    return descendants
  }

  if (isCategoryLoading || areAllCategoriesLoading) {
    return <Spinner />
  }

  if (!category || !allCategories) {
    return <Text>Category not found.</Text>
  }

  const descendantIds = getDescendants(categoryId, allCategories)
  const availableParents = allCategories.filter(
    (c) => c.id !== categoryId && !descendantIds.includes(c.id),
  )

  return (
    <Box>
      <Heading size="lg" mb={4}>
        Edit Category
      </Heading>
      <form onSubmit={handleSubmit(onSubmit)}>
        <VStack spacing={4} align="stretch">
          <FormControl isInvalid={!!errors.name}>
            <FormLabel htmlFor="name">Name</FormLabel>
            <Input
              id="name"
              {...register("name", {
                required: "Name is required",
              })}
              type="text"
            />
            {errors.name && (
              <FormErrorMessage>{errors.name.message}</FormErrorMessage>
            )}
          </FormControl>
          <FormControl isInvalid={!!errors.description}>
            <FormLabel htmlFor="description">Description</FormLabel>
            <Textarea id="description" {...register("description")} />
            {errors.description && (
              <FormErrorMessage>
                {errors.description.message}
              </FormErrorMessage>
            )}
          </FormControl>
          <FormControl isInvalid={!!errors.parent_category_id}>
            <FormLabel htmlFor="parent_category_id">Parent Category</FormLabel>
            <Select
              id="parent_category_id"
              {...register("parent_category_id")}
              placeholder="Select a parent category"
            >
              {availableParents.map((parent) => (
                <option key={parent.id} value={parent.id}>
                  {parent.name}
                </option>
              ))}
            </Select>
            {errors.parent_category_id && (
              <FormErrorMessage>
                {errors.parent_category_id.message}
              </FormErrorMessage>
            )}
          </FormControl>
          <Button type="submit" colorScheme="teal" isLoading={isSubmitting}>
            Update Category
          </Button>
        </VStack>
      </form>
    </Box>
  )
}
